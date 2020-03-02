[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Build Status](https://travis-ci.org/Tawasta/sale-workflow.svg?branch=12.0)](https://travis-ci.org/Tawasta/sale-workflow)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e3b9f2bc62a34626809482ba44fc8e90)](https://www.codacy.com/app/Tawasta/sale-workflow?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Tawasta/sale-workflow&amp;utm_campaign=Badge_Grade)

Odoo Sales, Workflow and Organization
=====================================

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[sale_crm_sale_order](sale_crm_sale_order/) | 12.0.1.0.0 | Integrates opportunities and quotations
[sale_customer_info_check](sale_customer_info_check/) | 12.0.1.0.0 | Enables confirming multiple sales at once
[sale_order_actual_delivery_date](sale_order_actual_delivery_date/) | 12.0.1.0.0 | Logs the date when all lines have been delivered
[sale_order_comment_lines](sale_order_comment_lines/) | 12.0.1.0.0 | Allow using comment lines in sale orders
[sale_order_confirmation_required_businessid](sale_order_confirmation_required_businessid/) | 12.0.1.0.0 | Prevents SO confirmation if customer has no business ID
[sale_order_confirmation_required_client_order_ref](sale_order_confirmation_required_client_order_ref/) | 12.0.1.0.0 | Prevents SO confirmation if customer reference is not set
[sale_order_confirmation_required_payment_term](sale_order_confirmation_required_payment_term/) | 12.0.1.0.0 | Prevents SO confirmation if customer has no payment terms set
[sale_order_confirmation_required_so_payment_term](sale_order_confirmation_required_so_payment_term/) | 12.0.1.0.0 | Prevents SO confirmation if SO has no payment term set
[sale_order_customer_contact](sale_order_customer_contact/) | 12.0.1.0.0 | Customer Contact for Sale Orders
[sale_order_customer_contact_no_popup](sale_order_customer_contact_no_popup/) | 12.0.1.0.0 | Removes the possibility to open partner form
[sale_order_customer_contact_show_address](sale_order_customer_contact_show_address/) | 12.0.1.0.0 | Show the contact address below the field
[sale_order_customer_order_number](sale_order_customer_order_number/) | 12.0.1.0.0 | New field for order number provided by customer
[sale_order_default_parent](sale_order_default_parent/) | 12.0.1.0.0 | Default parent for new invoice and shipping addresses
[sale_order_delivery_status](sale_order_delivery_status/) | 12.0.1.0.0 | Delivery information for Sales
[sale_order_description](sale_order_description/) | 12.0.1.0.0 | Adds a description (an internal note) to sale order
[sale_order_disposable_shipping_address](sale_order_disposable_shipping_address/) | 12.0.1.0.0 | Sale order shipping addresses can be deactivated after use
[sale_order_finalization_state](sale_order_finalization_state/) | 12.0.1.0.0 | New state for SOs between Quotation Sent and Sale Order
[sale_order_finalization_state_stock](sale_order_finalization_state_stock/) | 12.0.1.0.0 | Adds state-based readonly attributes to sale_stock SO fields
[sale_order_header](sale_order_header/) | 12.0.1.0.0 | New field for SO header/title
[sale_order_incoterm_extra_info](sale_order_incoterm_extra_info/) | 12.0.1.0.0 | New field for storing sale-specific incoterm info
[sale_order_line_copy](sale_order_line_copy/) | 12.0.1.0.0 | Sale order line copy
[sale_order_line_description_without_product](sale_order_line_description_without_product/) | 12.0.1.0.0 | Remove product and product code from default description
[sale_order_line_placeholder_product](sale_order_line_placeholder_product/) | 12.0.1.0.0 | Prevent Confirming Quotation With A Placeholder Product
[sale_order_line_stock_pickings](sale_order_line_stock_pickings/) | 12.0.1.0.0 | Show deliveries (stock pickings) on sale order lines
[sale_order_manufacturing_status](sale_order_manufacturing_status/) | 12.0.1.0.0 | Manufacturing Order information for Sales
[sale_order_mark_sent_button](sale_order_mark_sent_button/) | 12.0.1.0.0 | Printing a draft SO no longer moves it to Sent state
[sale_order_mass_cancel](sale_order_mass_cancel/) | 12.0.1.0.0 | Enables cancelling multiple sales at once
[sale_order_mass_confirm](sale_order_mass_confirm/) | 12.0.1.0.0 | Enables confirming multiple sales at once
[sale_order_migration_info](sale_order_migration_info/) | 12.0.1.0.0 | Helper fields for migration tracking
[sale_order_name_to_note](sale_order_name_to_note/) | 12.0.1.0.0 | Add sale order name to sale order note on order confirm
[sale_order_next_delivery_date](sale_order_next_delivery_date/) | 12.0.1.0.0 | Show the next open delivery date on sale order list view
[sale_order_no_open_form](sale_order_no_open_form/) | 12.0.1.0.0 | This module prevents to open forms on specified fields.
[sale_order_partner_disable_onchange](sale_order_partner_disable_onchange/) | 12.0.1.0.0 | Disable partner (customer) onchange on sale
[sale_order_partner_no_popups](sale_order_partner_no_popups/) | 12.0.1.0.0 | Removes the possibility to open partner forms from Sale
[sale_order_partner_onchange_suggest_partner_itself](sale_order_partner_onchange_suggest_partner_itself/) | 12.0.1.0.0 | Suggest customer itself instead of its sub-addresses
[sale_order_partner_quick_insert](sale_order_partner_quick_insert/) | 12.0.1.0.0 | Partner address fields as editable on sale order
[sale_order_partner_strict](sale_order_partner_strict/) | 12.0.1.0.0 | Only allow correct type and parent for addresses
[sale_order_partner_strict_with_partner_itself](sale_order_partner_strict_with_partner_itself/) | 12.0.1.0.0 | Allow customer itself or correct type and parent for address
[sale_order_project_in_header](sale_order_project_in_header/) | 12.0.1.0.0 | Moves analytic account to SO header and sets it as required
[sale_order_project_in_header_required](sale_order_project_in_header_required/) | 12.0.1.0.0 | Makes project in sale order header required
[sale_order_project_location_in_header](sale_order_project_location_in_header/) | 12.0.1.0.0 | Adds analytic account stock location to SO header
[sale_order_promised_delivery_date](sale_order_promised_delivery_date/) | 12.0.1.0.0 | Adds a new field for storing date of promised delivery
[sale_order_promised_delivery_date_in_calendar](sale_order_promised_delivery_date_in_calendar/) | 12.0.1.0.0 | Makes the sale order calendar utilize promised delivery date
[sale_order_promised_delivery_range](sale_order_promised_delivery_range/) | 12.0.1.0.0 | Adds new fields for storing date range of promised delivery
[sale_order_promised_delivery_range_helper](sale_order_promised_delivery_range_helper/) | 12.0.1.0.0 | Adds day and week selector helpers for date range
[sale_order_promised_delivery_range_in_calendar](sale_order_promised_delivery_range_in_calendar/) | 12.0.1.0.0 | Makes the sale order calendar utilize promised delivery range
[sale_order_promised_delivery_range_in_list](sale_order_promised_delivery_range_in_list/) | 12.0.1.0.0 | Makes the sale order list show promised delivery range
[sale_order_promised_delivery_range_to_picking](sale_order_promised_delivery_range_to_picking/) | 12.0.1.0.0 | Adds promised delivery range to stock picking
[sale_order_quick_return](sale_order_quick_return/) | 12.0.1.0.0 | Create returns from sale order lines
[sale_order_requested_delivery_date](sale_order_requested_delivery_date/) | 12.0.1.0.0 | Adds a new field for storing date of requested delivery
[sale_order_salesperson_to_note](sale_order_salesperson_to_note/) | 12.0.1.0.0 | Add salesperson to sale order note on order confirm
[sale_order_show_addresses](sale_order_show_addresses/) | 12.0.1.0.0 | Show the addresses below the fields
[sale_order_show_only_companies](sale_order_show_only_companies/) | 12.0.1.0.0 | SO's partner dropdown shows only companies
[sale_order_show_purchase_order](sale_order_show_purchase_order/) | 12.0.1.0.0 | Show Linked Purchase Orders on Sale Orders
[sale_order_stock_picking_auto_return](sale_order_stock_picking_auto_return/) | 12.0.1.0.0 | Ask to return delivered products when cancelling a sale
[sale_order_stock_warning_disable](sale_order_stock_warning_disable/) | 12.0.1.0.0 | No out-of-stock warning when adding products to SO lines
[sale_order_to_opportunity](sale_order_to_opportunity/) | 12.0.1.0.0 | Allows creating opportunities from sales
[sale_order_unlock](sale_order_unlock/) | 12.0.1.0.0 | Allows unlocking locked sale orders for managers
[sale_order_weight](sale_order_weight/) | 12.0.1.0.0 | Add weight on sale order and sale order lines
[sale_partner_default_note](sale_partner_default_note/) | 12.0.1.0.0 | Add a default sale note (terms and conditions) for partner
[sale_stock_availability](sale_stock_availability/) | 12.0.1.0.0 | Add product availability to SO line
[sale_stock_availability_unreserved](sale_stock_availability_unreserved/) | 12.0.1.0.0 | Add product unreserved availability to SO line


Unported addons
---------------
addon | version | summary
--- | --- | ---
[sale_order_confirmation_required_partner_fields](sale_order_confirmation_required_partner_fields/) | 12.0.1.0.0 (unported) | Configurable fields that must be set before sale is confirmed
[sale_order_contract_mandatory](sale_order_contract_mandatory/) | 12.0.1.0.0 (unported) | Make sale order contracts mandatory for sales persons

[//]: # (end addons)
