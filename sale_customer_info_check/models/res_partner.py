# -*- coding: utf-8 -*-
from odoo import models, fields
import datetime
from odoo.tools.translate import _

class partner(models.Model):

    _inherit = 'res.partner'
    
    info_verification_date = fields.Date('Partner info verified on')
    