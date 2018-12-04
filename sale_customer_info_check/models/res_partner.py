# -*- coding: utf-8 -*-
from odoo import models, fields


class partner(models.Model):

    _inherit = 'res.partner'

    info_verification_date = fields.Date('Partner info verified on')
