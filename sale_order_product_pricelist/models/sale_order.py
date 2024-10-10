from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for record in self:
            pricelists = record.order_line.mapped("product_id.pricelist_id")

            if pricelists:
                if len(pricelists) > 1:
                    _logger.warning("Multiple pricelists found!")
                    _logger.warning(
                        "Pricelist priorities are not supported, using the first one"
                    )
                pricelist_id = pricelists[0]

                if record.partner_id.property_product_pricelist != pricelist_id:
                    _logger.info(
                        "Setting pricelist '{}' to '{}'".format(
                            pricelist_id.name, record.partner_id.name
                        )
                    )
                    record.partner_id.property_product_pricelist = pricelist_id

        return super().action_confirm()
