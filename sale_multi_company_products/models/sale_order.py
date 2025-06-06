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
        """
        Returns the base domain that all programs have to comply to.
        Now expanded to include products' companies as well for multi-company promo codes.
        """
        self.ensure_one()
        today = fields.Date.context_today(self)

        # Haetaan tilauksen tuotteiden yritykset
        product_company_ids = self.order_line.mapped('product_id.company_id.id')

        # Sallitaan yritykset: tilauksen yritys + sen emoyritys + tuotteiden yritykset
        allowed_company_ids = list(set([self.company_id.id, self.company_id.parent_id.id] + product_company_ids))

        return [('active', '=', True), ('sale_ok', '=', True),
                *self.env['loyalty.program']._check_company_domain(allowed_company_ids),
                '|', ('pricelist_ids', '=', False), ('pricelist_ids', 'in', [self.pricelist_id.id]),
                '|', ('date_from', '=', False), ('date_from', '<=', today),
                '|', ('date_to', '=', False), ('date_to', '>=', today)]

    def _get_trigger_domain(self):
        """
        Returns the base domain that all triggers have to comply to.
        Now expanded to include products' companies as well for multi-company promo codes.
        """
        self.ensure_one()
        today = fields.Date.context_today(self)

        product_company_ids = self.order_line.mapped('product_id.company_id.id')
        allowed_company_ids = list(set([self.company_id.id, self.company_id.parent_id.id] + product_company_ids))

        return [('active', '=', True), ('program_id.sale_ok', '=', True),
                *self.env['loyalty.program']._check_company_domain(allowed_company_ids),
                '|', ('program_id.pricelist_ids', '=', False),
                     ('program_id.pricelist_ids', 'in', [self.pricelist_id.id]),
                '|', ('program_id.date_from', '=', False), ('program_id.date_from', '<=', today),
                '|', ('program_id.date_to', '=', False), ('program_id.date_to', '>=', today)]

    def _try_apply_code(self, code):
        self.ensure_one()

        base_domain = self._get_trigger_domain()
        domain = expression.AND([base_domain, [('mode', '=', 'with_code'), ('code', '=', code)]])
        rule = self.env['loyalty.rule'].search(domain)
        program = rule.program_id
        coupon = False

        if rule in self.code_enabled_rule_ids:
            return {'error': _('This promo code is already applied.')}

        # Ei löytynyt triggeriä -> etsitään kuponki
        if not program:
            coupon = self.env['loyalty.card'].search([('code', '=', code)])
            if not coupon or\
                not coupon.program_id.active or\
                not coupon.program_id.reward_ids or\
                not coupon.program_id.filtered_domain(self._get_program_domain()):
                return {'error': _('This code is invalid (%s).', code), 'not_found': True}
            elif coupon.expiration_date and coupon.expiration_date < fields.Date.today():
                return {'error': _('This coupon is expired.')}
            elif coupon.points < min(coupon.program_id.reward_ids.mapped('required_points')):
                return {'error': _('This coupon has already been used.')}
            program = coupon.program_id

        if not program or not program.active:
            return {'error': _('This code is invalid (%s).', code), 'not_found': True}
        elif (program.limit_usage and program.total_order_count >= program.max_usage):
            return {'error': _('This code is expired (%s).', code)}

        # Lisätään rule, jos löytyy
        if rule:
            self.code_enabled_rule_ids |= rule

        program_is_applied = program in self._get_points_programs()

        if coupon:
            self.applied_coupon_ids += coupon

        # Tarkistetaan, onko ostoskorissa tuotteita, jotka kuuluvat ohjelman yritykseen
        matching_lines = self.order_line.filtered(lambda l: l.product_id.company_id == program.company_id)
        if not matching_lines:
            # Ei tuotteita ohjelman yrityksestä, mutta sallitaan moniyritysbypass
            # Voit halutessasi lisätä tähän loggausta tai erityiskäsittelyn
            pass

        if program_is_applied:
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

        return self._get_claimable_rewards(forced_coupons=coupon)



