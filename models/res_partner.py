# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import exceptions
from openerp.exceptions import ValidationError
from openerp import _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange('businessid')
    def onchange_businessid(self):
        # Reformat business id
        if isinstance(self.businessid, basestring) and re.match('^[0-9]{8}$', self.businessid):
            self.businessid = self.businessid[:7] + '-' + self.businessid[7:]

        if self._check_businessid():
            self.update_vat(self.businessid)

    @api.one
    @api.constrains('businessid')
    def _check_businessid(self):
        # Validate the business id
        self.validate_business_id(self.businessid)

        partners = []

        if 'default_parent_id' in self._context:
            self.parent_id = self._context['default_parent_id']

        if not isinstance(self.id, models.NewId):
            partners.append(self.id)

        if self.parent_id:
            # Get the top company and all its children
            parent = self._get_recursive_parent()[0]
            children = self._get_recursive_child_ids(parent)

            partners.extend(children)
            partners.append(parent.id)

        # Check if a company with this business id already exists
        existing_partner = self.env['res.partner'].search([
            ('businessid', '=', self.businessid),
            ('businessid', '!=', False),
            ('id', 'not in', partners),
            ],
            limit=1,
        )

        if existing_partner:
            msg = _("This business id is already in use for '%s'!") % existing_partner.name
            raise ValidationError(msg) \

    @api.one
    @api.constrains('vat')
    def _check_vat(self):
        partners = []

        if not isinstance(self.id, models.NewId):
            partners.append(self.id)

        if self.parent_id:
            # Get the top company and all its children
            parent = self._get_recursive_parent()[0]
            children = self._get_recursive_child_ids(parent)

            partners.extend(children)
            partners.append(parent.id)

        # Check if a company with this vat already exists
        existing_partner = self.env['res.partner'].search([
            ('vat', '=', self.vat),
            ('vat', '!=', False),
            ('id', 'not in', partners),
            ],
            limit=1,
        )

        if existing_partner:
            msg = _("This VAT is already in use for '%s'!") % existing_partner.name
            raise ValidationError(msg)

    ''' Override existing sql constraint with one that always returns true '''
    _sql_constraints = [('businessid_unique', 'CHECK(1=1)', 'This business id is already in use')]

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    def validate_business_id(self, businessid):
        # Validates business ID format
        if not businessid:
            return False

        '''
        Regular Finnish business id (y-tunnus)
        Format '1234567-1'
        OR
        Registered association (rekisteröity yhdistys, ry/r.y.).
        Format 123.456
        '''
        if not re.match('^[0-9]{7}[-][0-9]{1}$', businessid) and not re.match('^[0-9]{3}[.][0-9]{3}$', businessid):
            msg = _("Invalid business id!") + " " + _("Please use format '1234567-1' or '123.456'")
            raise ValidationError(msg)
            return False

    def update_vat(self, businessid):
        # Auto-update VAT
        if not self.businessid:
            return False

        #TODO: Split this into country code-specific methods

        if self.country_id.code == 'FI':
            self.vat = "FI" + self.businessid.replace('-', '')
