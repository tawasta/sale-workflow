from odoo import http
from odoo.http import request

class SaleOrderLineConfiguratorController(http.Controller):
    
    @http.route('/sale_order_line_configurator/xmlid_to_res_id', type='json', auth='user')
    def xmlid_to_res_id(self, xmlid):
        try:
            print("IN CONTROLLER TRY!")
            # Try to find the record based on the xmlid
            record = request.env.ref(xmlid)
            return record.id
        except ValueError:
            print("IN CONTROLLER EXCEPT!")
            # If the record isn't found, return False
            return False