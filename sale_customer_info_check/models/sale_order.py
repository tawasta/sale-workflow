# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import ValidationError
import datetime


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_info_msg = fields.Char(compute='_get_customer_info_msg', size=256,
                                   string="Customer info status")

    ''' How old the customer info can be before it gets flagged '''
    _DAY_THRESHOLD = 90

    def write(self, values):

        if 'state' in values:
            if values['state'] in ['progress', 'manual']:
                partner_id = self.browse()[0].partner_id.id

                res = self._read_customer_vat_businessid_info(partner_id)
                if res != 'OK':
                    raise ValidationError(_('Error: %s') % res)

        return super(SaleOrder, self).write(values)

    def _read_customer_uptodate_info(self, selected_partner_id):
        partner_model = self.env['res.partner']

        partner = partner_model.browse([selected_partner_id])[0]

        info_update_date = partner.info_verification_date

        if info_update_date is False:
            return ("Not verified")

        updated = datetime.datetime.strptime(info_update_date, '%Y-%m-%d')

        now = datetime.datetime.now()

        delta = now - updated
        day_difference = delta.days

        if day_difference >= self._DAY_THRESHOLD:
            return ("Outdated - verified more than ") + str
            (self._DAY_THRESHOLD) + " " + ('days ago')
        else:
            return ('Verified on ') + updated.strftime("%Y-%m-%d")

    def _read_customer_vat_businessid_info(self, selected_partner_id):
        partner_model = self.env['res.partner']

        partner = partner_model.browse([selected_partner_id])[0]

        partner_country_id = partner.country_id.id

        missing_info = []

        if partner_country_id is False:
            missing_info.append(('Country'))
        else:

            country_obj = self.env['res.country']
            selected_country = country_obj.browse([partner_country_id])[0]

            name = selected_country['name']

            b_id_check_countries = ['Finland']

            businessid_required = False
            vat_required = False

            if name in b_id_check_countries and partner.is_company:
                businessid_required = True

            ''' List of all countries that trigger the vat condition. '''
            vat_check_countries = ['Austria', 'Belgium', 'Bulgaria',
                                   'Croatia', 'Cyprus', 'Czech Republic',
                                   'Denmark', 'Estonia', 'Finland',
                                   'France', 'Germany', 'Greece',
                                   'Hungary', 'Ireland', 'Italy',
                                   'Latvia', 'Lithuania', 'Luxembourg',
                                   'Malta', 'Netherlands', 'Poland',
                                   'Portugal', 'Romania', 'Slovakia',
                                   'Slovenia', 'Spain', 'Sweden',
                                   'United Kingdom']

            if name in vat_check_countries and partner.is_company:
                vat_required = True

            if partner.businessid is False and businessid_required is True:
                missing_info.append(('Business ID'))

            if partner.vat is False and vat_required is True:
                missing_info.append(('VAT'))

        if len(missing_info) > 0:
            return ('Missing information: ') + ",".join(missing_info)
        else:
            return ('OK')

    def onchange_partner_id(self, partner_id):

        result = super(SaleOrder, self).onchange_partner_id(partner_id)

        if partner_id is False:
            result['value']['partner_info_msg'] = ""
        else:
            result['value']['partner_info_msg'] = \
                self._read_customer_uptodate_info(partner_id)

        return result

    def _get_customer_info_msg(self, field_name, arg):
        res = {}
        for sale_order in self.browse():
            selected_partner_id = sale_order.partner_id.id
            info_msg = self._read_customer_uptodate_info(selected_partner_id)
            res[sale_order.id] = info_msg
        return res
