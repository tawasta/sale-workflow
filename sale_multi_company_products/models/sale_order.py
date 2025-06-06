from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools.float_utils import float_is_zero, float_round
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    current_invoice_company_id = fields.Many2one(
        string="Current company to invoice",
        help="This field is for technical use only",
        comodel_name="res.company",
        readonly=True,
        copy=False,
    )

    def _check_order_line_company_id(self):
        # Override cross-company product check
        return

    def _create_invoices(self, grouped=False, final=False, date=None):
        for order in self:
            lines = order._get_invoiceable_lines()

            companies = lines.mapped("product_id.company_id")
            if len(companies) == 1 and companies == self.company_id:
                # No custom processing for one company
                return super()._create_invoices(grouped, final, date)

            moves = self.env["account.move"]
            for company in companies:
                # Set a temporary company values
                order = order.with_company(company.id).with_context(
                    default_company_id=company.id
                )
                if order.partner_id.company_id:
                    # Partner can't belong to a company
                    order.partner_id.company_id = False

                if order.partner_invoice_id.company_id:
                    # Invoice partner can't belong to a company
                    order.partner_invoice_id.company_id = False

                if order.partner_shipping_id.company_id:
                    # Shipping partner can't belong to a company
                    order.partner_shipping_id.company_id = False

                order.current_invoice_company_id = company.id
                moves += super()._create_invoices(grouped, final, date)

            # Set the correct company and unset the temporary company
            order.current_invoice_company_id = False

        # Only return user company moves to prevent access error
        moves = moves.filtered(lambda r: r.company_id == self.env.user.company_id)

        return moves

    def _get_invoiceable_lines(self, final=False):
        lines = super()._get_invoiceable_lines(final)

        if self.current_invoice_company_id:
            lines = lines.filtered(
                lambda r: r.product_id.company_id == self.current_invoice_company_id
            )

        return lines

    def _prepare_invoice(self):
        if self.current_invoice_company_id:
            company = self.current_invoice_company_id
            self = self.with_company(company.id).with_context(
                default_company_id=company.id
            )

        invoice_vals = super()._prepare_invoice()
        if self.current_invoice_company_id:
            invoice_vals["company_id"] = self.current_invoice_company_id.id
            invoice_vals["partner_bank_id"] = company.partner_id.bank_ids[:1].id
            fiscal_position_model = self.env["account.fiscal.position"]
            old_fiscal_position = fiscal_position_model.browse(
                [invoice_vals["fiscal_position_id"]]
            )

            fiscal_position = fiscal_position_model.sudo().search(
                [
                    ("company_id", "=", company.id),
                    ("name", "=", old_fiscal_position.name),
                ]
            )
            if fiscal_position:
                invoice_vals["fiscal_position_id"] = fiscal_position.id

        return invoice_vals

    def _get_reward_line_values(self, reward, coupon, **kwargs):
        res = super()._get_reward_line_values(reward, coupon, **kwargs)

        for line in res:
            # The company will default to incorrect company,
            # if product company differs from order company
            line["company_id"] = self.company_id.id

        return res

    def _get_program_domain(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        allowed_company_ids = [self.company_id.id]
        if self.company_id.parent_id:
            allowed_company_ids.append(self.company_id.parent_id.id)

        # Lisää myös tuotteiden yritykset mukaan
        product_company_ids = self.order_line.mapped('product_id.company_id.id')
        allowed_company_ids += product_company_ids

        # Poista duplikaatit ja None-arvot
        allowed_company_ids = list(set(filter(None, allowed_company_ids)))

        return [('active', '=', True), ('sale_ok', '=', True),
                *self.env['loyalty.program']._check_company_domain(allowed_company_ids),
                '|', ('pricelist_ids', '=', False), ('pricelist_ids', 'in', [self.pricelist_id.id]),
                '|', ('date_from', '=', False), ('date_from', '<=', today),
                '|', ('date_to', '=', False), ('date_to', '>=', today)]


    def _get_trigger_domain(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        allowed_company_ids = [self.company_id.id]
        if self.company_id.parent_id:
            allowed_company_ids.append(self.company_id.parent_id.id)

        # Lisää myös tuotteiden yritykset mukaan
        product_company_ids = self.order_line.mapped('product_id.company_id.id')
        allowed_company_ids += product_company_ids

        allowed_company_ids = list(set(filter(None, allowed_company_ids)))

        return [('active', '=', True), ('program_id.sale_ok', '=', True),
                *self.env['loyalty.program']._check_company_domain(allowed_company_ids),
                '|', ('program_id.pricelist_ids', '=', False),
                     ('program_id.pricelist_ids', 'in', [self.pricelist_id.id]),
                '|', ('program_id.date_from', '=', False), ('program_id.date_from', '<=', today),
                '|', ('program_id.date_to', '=', False), ('program_id.date_to', '>=', today)]

    def _filter_claimable_rewards_by_company(self, rewards):
        allowed_company_ids = [self.company_id.id]
        if self.company_id.parent_id:
            allowed_company_ids.append(self.company_id.parent_id.id)
        product_company_ids = self.order_line.mapped('product_id.company_id.id')
        allowed_company_ids += product_company_ids
        allowed_company_ids = list(set(filter(None, allowed_company_ids)))

        # Suodata rewards, joilla on ohjelma, joka kuuluu allowed_company_ids
        return rewards.filtered(lambda r: r.program_id.company_id.id in allowed_company_ids)

    def _try_apply_code(self, code):
        """
        Tries to apply a promotional code to the sales order.
        It can be either from a coupon or a program rule.

        Returns a dict with the following possible keys:
         - 'not_found': Populated with True if the code did not yield any result.
         - 'error': Any error message that could occur.
         OR The result of `_get_claimable_rewards` with the found or newly created coupon,
         it will be empty if the coupon was consumed completely.
        """
        self.ensure_one()

        base_domain = self._get_trigger_domain()
        domain = expression.AND([base_domain, [('mode', '=', 'with_code'), ('code', '=', code)]])
        rule = self.env['loyalty.rule'].search(domain, limit=1)  # hae yksi sääntö koodilla
        program = rule.program_id if rule else False
        coupon = False

        if rule and rule in self.code_enabled_rule_ids:
            return {'error': _('This promo code is already applied.')}

        # Jos sääntöä ei löytynyt, yritä etsiä kuponki
        if not program:
            coupon = self.env['loyalty.card'].search([('code', '=', code)], limit=1)
            if not coupon:
                return {'error': _('This code is invalid (%s).', code), 'not_found': True}

            program = coupon.program_id
            # Validointi, että ohjelma on aktiivinen ja oikea
            if not program or not program.active:
                return {'error': _('This code is invalid (%s).', code), 'not_found': True}

            # Tarkistetaan, että kuponkiohjelma löytyy myös tämän myyntitilauksen domainilta
            if not coupon.program_id.reward_ids or not coupon.program_id.filtered_domain(self._get_program_domain()):
                return {'error': _('This code is invalid (%s).', code), 'not_found': True}

            # Tarkistetaan kuponki vanhentuminen ja käyttöoikeus
            if coupon.expiration_date and coupon.expiration_date < fields.Date.today():
                return {'error': _('This coupon is expired.')}
            if coupon.points < min(coupon.program_id.reward_ids.mapped('required_points')):
                return {'error': _('This coupon has already been used.')}

        # Tarkistetaan ohjelman käyttörajat (max usage jne)
        if program.limit_usage and program.total_order_count >= program.max_usage:
            return {'error': _('This code is expired (%s).', code)}

        # Lisätään sääntö käyttöön, jos löytyi
        if rule:
            self.code_enabled_rule_ids |= rule

        program_is_applied = program in self._get_points_programs()

        if coupon:
            self.applied_coupon_ids += coupon

        if program_is_applied:
            # Päivitetään pisteet ja palkinnot, kun ohjelma on jo käytössä
            self._update_programs_and_rewards()
        elif program.applies_on != 'future' or not coupon:
            apply_result = self._try_apply_program(program, coupon)
            if 'error' in apply_result and (not program.is_nominative or (program.is_nominative and not coupon)):
                if rule:
                    self.code_enabled_rule_ids -= rule
                if coupon and not apply_result.get('already_applied', False):
                    self.applied_coupon_ids -= coupon
                return apply_result
            coupon = apply_result.get('coupon', self.env['loyalty.card'])

        result = self._get_claimable_rewards(forced_coupons=coupon)
        result = self._filter_claimable_rewards_by_company(result)
        return result




