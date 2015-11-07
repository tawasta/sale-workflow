# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import exceptions

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

        self.validate_business_id(self.businessid)

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    def validate_business_id(self, businessid):
        if not businessid:
            return True

        '''
        Regular Finnish business id (y-tunnus)
        Format '1234567-1'
        OR
        Registered association (rekisteröity yhdistys, ry/r.y.).
        Format 123.456
        '''
        if not re.match('^[0-9]{7}[-][0-9]{1}$', businessid) and not re.match('^[0-9]{3}[.][0-9]{3}$', businessid):
            raise exceptions.Warning("Invalid business id!" + " " + "Please use format '1234567-1' or '123.456'")
            return False