[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Pre-commit Status](https://github.com/tawasta/sale-workflow/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/tawasta/sale-workflow/actions/workflows/pre-commit.yml?query=branch%3A17.0)

Sale Workflow
=============
Sale Workflow Addons for Odoo.

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_multi_company_products](sale_multi_company_products/) | 17.0.1.1.0 |  | Allows selling multiple company products on a single sale
[sale_order_additional_note](sale_order_additional_note/) | 17.0.1.0.1 |  | Adds Html-type field to Sale Order, which is shown on its PDF print
[sale_order_address_details](sale_order_address_details/) | 17.0.1.0.0 |  | Sale order address details
[sale_order_analytic_distribution_required_upon_invoice](sale_order_analytic_distribution_required_upon_invoice/) | 17.0.1.0.0 |  | Creating an invoice from SO is not possible if analytic distributions are not set on lines
[sale_order_country_group_delivery_terms](sale_order_country_group_delivery_terms/) | 17.0.1.0.2 |  | Add note from country groups to SO when confirming the sale
[sale_order_country_group_text](sale_order_country_group_text/) | 17.0.1.0.0 |  | Get report text from country groups setting
[sale_order_customer_contact](sale_order_customer_contact/) | 17.0.1.0.2 |  | Customer Contact for Sale Orders
[sale_order_customer_contact_to_narration](sale_order_customer_contact_to_narration/) | 17.0.1.0.0 |  | Adds contact name to invoice as an extra information
[sale_order_customer_is_company](sale_order_customer_is_company/) | 17.0.1.0.0 |  | Select only customers that are companies to sale orders
[sale_order_customer_order_date](sale_order_customer_order_date/) | 17.0.1.0.0 |  | Customer order date field to sale order
[sale_order_delivery_date_to_invoice](sale_order_delivery_date_to_invoice/) | 17.0.1.0.0 |  | Pre-fill invoice delivery date from Sale Order
[sale_order_delivery_place](sale_order_delivery_place/) | 17.0.1.0.0 |  | Delivery Terms on Sale Order
[sale_order_delivery_term](sale_order_delivery_term/) | 17.0.1.0.1 |  | Sale Order Delivery term
[sale_order_description](sale_order_description/) | 17.0.1.0.0 |  | Adds a description (an internal note) to sale order
[sale_order_description_to_invoice](sale_order_description_to_invoice/) | 17.0.1.0.0 |  | Moves the SO description to invoice description when creating an invoice
[sale_order_description_to_stock_picking](sale_order_description_to_stock_picking/) | 17.0.1.0.0 |  | Adds sale order description to stock picking
[sale_order_duplicate_customer_reference](sale_order_duplicate_customer_reference/) | 17.0.1.0.0 |  | When duplicating also copy customer reference
[sale_order_enable_delivery_address_as_company](sale_order_enable_delivery_address_as_company/) | 17.0.1.0.0 |  | Enable to automatically set Delivery address even if it is a company
[sale_order_force_note_line_to_be_invoiced](sale_order_force_note_line_to_be_invoiced/) | 17.0.1.0 |  | Move SO line notes to invoice
[sale_order_header_text](sale_order_header_text/) | 17.0.1.0.0 |  | New field for SO header/title
[sale_order_hide_proforma_in_form_view](sale_order_hide_proforma_in_form_view/) | 17.0.1.0.1 |  | Hides PRO-FORMA button in Sale Order form view
[sale_order_line_copy](sale_order_line_copy/) | 17.0.1.0.0 |  | Duplicate single order lines or sections on sale order
[sale_order_line_copy_purchase_price](sale_order_line_copy_purchase_price/) | 17.0.1.0.0 |  | Enable to copy Cost-field (purchase_price) when copying a SO line
[sale_order_line_decription_to_stock_move](sale_order_line_decription_to_stock_move/) | 17.0.1.0.0 |  | Description -field info of SO line is moved to stock.move Description
[sale_order_line_delivery_date_split_picking](sale_order_line_delivery_date_split_picking/) | 17.0.1.0.0 |  | Add picking date to SO lines and split lines to pickings
[sale_order_line_delivery_time](sale_order_line_delivery_time/) | 17.0.1.0.0 |  | Sale Order Line Delivery Time
[sale_order_line_forecasted_available](sale_order_line_forecasted_available/) | 17.0.1.0.0 |  | Add virtual_available field to sale order line
[sale_order_line_limit](sale_order_line_limit/) | 17.0.1.0.0 |  | Increase number of SO lines shown before needing to use pager
[sale_order_line_product_internal_reference](sale_order_line_product_internal_reference/) | 17.0.1.0.0 |  | Product internal reference is shown on form lines
[sale_order_line_product_name](sale_order_line_product_name/) | 17.0.1.0.0 |  | Product name -field is shown on form lines
[sale_order_line_qty_available](sale_order_line_qty_available/) | 17.0.1.0.0 |  | Add qty_available to sale order line
[sale_order_line_tax_info_to_note_field](sale_order_line_tax_info_to_note_field/) | 17.0.1.0.1 |  | Writes Sale Order Lines' tax info to SO's Note field
[sale_order_margin_manual_cost](sale_order_margin_manual_cost/) | 17.0.1.0.0 |  | Disable automated cost update from SO lines
[sale_order_mass_confirm](sale_order_mass_confirm/) | 17.0.1.0.0 |  | Enables confirming multiple sales at once
[sale_order_partner_delivery_method](sale_order_partner_delivery_method/) | 17.0.1.0.0 |  | Delivery method is assigned based on partner's delivery method
[sale_order_partner_tag_to_crm_tag](sale_order_partner_tag_to_crm_tag/) | 17.0.1.0.0 |  | Tag from partner category to sale order CRM tag
[sale_order_pricelist_price_by_categ_qty](sale_order_pricelist_price_by_categ_qty/) | 17.0.1.0.0 |  | Set sale order line price by pricelist quantities
[sale_order_product_pricelist](sale_order_product_pricelist/) | 17.0.1.0.1 |  | If product has a pricelist, use it for SO lines
[sale_order_proforma_country_group_text](sale_order_proforma_country_group_text/) | 17.0.1.0.0 |  | Get report text from country groups setting
[sale_order_project_in_header](sale_order_project_in_header/) | 17.0.1.0.0 |  | Moves analytic account to SO header
[sale_order_project_location_in_header](sale_order_project_location_in_header/) | 17.0.1.0.0 |  | Adds analytic account stock location to SO header
[sale_order_promised_delivery_range](sale_order_promised_delivery_range/) | 17.0.1.0.0 |  | Adds new fields for storing date range of promised delivery
[sale_order_requested_delivery_date](sale_order_requested_delivery_date/) | 17.0.1.0.0 |  | Adds a new field for storing date of requested delivery
[sale_order_require_payment_field_copy_fix](sale_order_require_payment_field_copy_fix/) | 17.0.1.0.0 |  | Recalculate the 'Online payment' field value when duplicating SO
[sale_order_sale_type](sale_order_sale_type/) | 17.0.1.0.0 |  | Sale Type field is added to sales
[sale_order_search_multi_value](sale_order_search_multi_value/) | 17.0.1.0.0 |  | Search sale orders with a list of sale order names
[sale_order_show_addresses](sale_order_show_addresses/) | 17.0.1.0.0 |  | Show the addresses below their fields
[sale_order_show_purchase_order](sale_order_show_purchase_order/) | 17.0.1.0.0 |  | Show Linked Purchase Orders on Sale Orders
[sale_order_template_disable_note_auto_reload](sale_order_template_disable_note_auto_reload/) | 17.0.1.0.0 |  | Don't auto-reload SO template note when changing a partner
[sale_order_tree_customer_reference](sale_order_tree_customer_reference/) | 17.0.1.0.0 |  | Add customer reference to sale order tree view
[sale_order_tree_view_quotations_only](sale_order_tree_view_quotations_only/) | 17.0.1.0.0 |  | Sale Quotations tree view - Show only quotations
[sale_order_warehouse_do_not_copy](sale_order_warehouse_do_not_copy/) | 17.0.1.0.0 |  | Do not copy a warehouse when copying a sale order
[sale_order_warranty](sale_order_warranty/) | 17.0.1.0.1 |  | Sale Order Warranty
[sale_order_week_of_shipment](sale_order_week_of_shipment/) | 17.0.1.0.0 |  | Week of shipment field to sale order
[sale_order_year_of_shipment](sale_order_year_of_shipment/) | 17.0.1.0.0 |  | Sale Order year from commitment date
[sale_payment_acquirer_optional_so_reference](sale_payment_acquirer_optional_so_reference/) | 17.0.1.0.0 |  | Adds an option to not create a payment reference for SO
[sale_stock_availability_unreserved](sale_stock_availability_unreserved/) | 17.0.1.0.0 |  | Add product unreserved availability to SO line
[sale_stock_client_ref_to_picking](sale_stock_client_ref_to_picking/) | 17.0.1.0.0 |  | Move SO customer reference to created stock pickings

[//]: # (end addons)
