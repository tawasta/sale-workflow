from odoo import models


class ResPartner(models.Model):

    _inherit = "res.partner"

    def create_stock_location(self):
        self.ensure_one()

        default_location = self.env.ref("stock.stock_location_customers")
        if (
            self.property_stock_customer
            and self.property_stock_customer != default_location
        ):
            # A custom location already exists
            return self.property_stock_customer

        # If partner doesn't have own location, create one
        StockLocation = self.env["stock.location"]

        # partner_id removed from domain in the 14.0 version
        customer_location = StockLocation.search(
            [
                ("company_id", "=", self.company_id.id),
                ("usage", "=", "customer"),
            ],
            limit=1,
        )

        if not customer_location:
            if self.parent_id:
                if not self.parent_id.property_stock_customer:
                    # Auto-create parent stock location
                    self.parent_id.create_stock_location()

                default_location = self.parent_id.property_stock_customer

            location_values = {
                "name": self.name,
                "usage": "customer",
                "location_id": default_location.id,
                "company_id": self.company_id.id,
            }

            customer_location = StockLocation.sudo().create(location_values)

        self.property_stock_customer = customer_location

        return customer_location
