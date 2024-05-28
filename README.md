[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Pipeline Status](https://gitlab.com/tawasta/odoo/sale-workflow/badges/14.0-dev/pipeline.svg)](https://gitlab.com/tawasta/odoo/sale-workflow/-/pipelines/)

Sale Workflow
=============
Sale Workflow Addons for Odoo.

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[sale_blanket_order_forecast](sale_blanket_order_forecast/) | 14.0.1.1.17 |  | Allows making forecast sale orders from blanket orders
[sale_blanket_order_kit](sale_blanket_order_kit/) | 14.0.1.2.1 |  | Add kits and expand them as forecast lines
[sale_customer_default_my](sale_customer_default_my/) | 14.0.1.0.0 |  | Show my customers by default on Customer list view
[sale_customers_no_default_filter](sale_customers_no_default_filter/) | 14.0.1.0.0 |  | Remove Customers default filter
[sale_multi_company](sale_multi_company/) | 14.0.1.2.0 |  | Allows selling multiple company products on a single sale
[sale_order_address_details](sale_order_address_details/) | 14.0.1.0.0 |  | Sale order address details
[sale_order_carrier_in_list](sale_order_carrier_in_list/) | 14.0.1.0.0 |  | Add carrier to list view
[sale_order_commitment_date_header](sale_order_commitment_date_header/) | 14.0.1.0.0 |  | Move Commitment Date to header
[sale_order_compute_weight](sale_order_compute_weight/) | 14.0.1.0.0 |  | Add weight on sale order and sale order lines
[sale_order_confirmation_required_businessid](sale_order_confirmation_required_businessid/) | 14.0.1.1.0 |  | Prevents SO confirmation if customer has no business ID
[sale_order_confirmation_required_client_order_ref](sale_order_confirmation_required_client_order_ref/) | 14.0.1.1.0 |  | Prevents SO confirmation if customer reference is not set
[sale_order_confirmation_required_payment_term](sale_order_confirmation_required_payment_term/) | 14.0.1.1.0 |  | Prevents SO confirmation if customer has no payment terms set
[sale_order_confirmation_required_so_payment_term](sale_order_confirmation_required_so_payment_term/) | 14.0.1.0.0 |  | Prevents SO confirmation if SO has no payment term set
[sale_order_country_group_text](sale_order_country_group_text/) | 14.0.1.0.0 |  | Get report text from country groups setting
[sale_order_customer_contact](sale_order_customer_contact/) | 14.0.1.1.4 |  | Customer Contact for Sale Orders
[sale_order_customer_contact_show_address](sale_order_customer_contact_show_address/) | 14.0.1.0.0 |  | Show the contact address below the field
[sale_order_customer_contact_to_narration](sale_order_customer_contact_to_narration/) | 14.0.1.0.0 |  | Adds contact name to invoice as an extra information
[sale_order_customer_order_date](sale_order_customer_order_date/) | 14.0.1.0.0 |  | Customer order date field to sale order
[sale_order_customer_order_number](sale_order_customer_order_number/) | 14.0.1.0.0 |  | New field for order number provided by customer
[sale_order_customer_reference_header](sale_order_customer_reference_header/) | 14.0.1.0.0 |  | Move Customer reference to header
[sale_order_default_parent](sale_order_default_parent/) | 14.0.1.0.0 |  | Default parent for new invoice and shipping addresses on SO
[sale_order_delivery_date_to_invoice](sale_order_delivery_date_to_invoice/) | 14.0.1.0.0 |  | Pre-fill invoice delivery date from Sale Order
[sale_order_delivery_place](sale_order_delivery_place/) | 14.0.1.0.0 |  | Delivery Terms on Sale Order
[sale_order_delivery_status](sale_order_delivery_status/) | 14.0.1.0.0 |  | Delivery information for Sales
[sale_order_delivery_term](sale_order_delivery_term/) | 14.0.1.0.0 |  | Sale Order Delivery term
[sale_order_description](sale_order_description/) | 14.0.1.0.0 |  | Adds a description (an internal note) to sale order
[sale_order_description_to_invoice](sale_order_description_to_invoice/) | 14.0.1.0.0 |  | Moves the SO description to invoice description
[sale_order_description_to_stock_picking](sale_order_description_to_stock_picking/) | 14.0.1.0.0 |  | Adds sale order description to stock picking
[sale_order_disposable_shipping_address](sale_order_disposable_shipping_address/) | 14.0.1.0.0 |  | Sale order shipping addresses can be deactivated after use
[sale_order_duplicate_customer_reference](sale_order_duplicate_customer_reference/) | 14.0.1.0.0 |  | When duplicating also copy customer reference
[sale_order_email_wizard_default_to_confirmation_template](sale_order_email_wizard_default_to_confirmation_template/) | 14.0.1.0.0 |  | Sale Order Email Wizard suggests the confirmation template also for quotations
[sale_order_enable_delivery_address_as_company](sale_order_enable_delivery_address_as_company/) | 14.0.1.0.0 |  | Enable to automatically set Delivery address even if it is a company
[sale_order_excel_import](sale_order_excel_import/) | 14.0.1.0.0 |  | Import Sale orders with excel file
[sale_order_handler](sale_order_handler/) | 14.0.1.0.0 |  | Handler on SO, invoice and picking
[sale_order_header](sale_order_header/) | 14.0.1.0.2 |  | New field for SO header/title
[sale_order_header_fiscal_position_warehouse_incoterm](sale_order_header_fiscal_position_warehouse_incoterm/) | 14.0.1.0.0 |  | Move fiscal position, warehouse, and incoterm to so header
[sale_order_hide_send_by_email](sale_order_hide_send_by_email/) | 14.0.1.0.0 |  | Hide send by email button in sale order
[sale_order_invoice_advance_invoice_date_due](sale_order_invoice_advance_invoice_date_due/) | 14.0.1.0.0 |  | Sets advance invoice date due 14 days before order commitment date
[sale_order_invoice_status_color](sale_order_invoice_status_color/) | 14.0.1.0.0 |  | Sale order tree view status colors based on invoice state
[sale_order_line_amount_to_invoice](sale_order_line_amount_to_invoice/) | 14.0.1.0.0 |  | Sale order line tree - Untaxed Amount To Invoice
[sale_order_line_commitment_date](sale_order_line_commitment_date/) | 14.0.1.1.0 |  | Add picking date to SO lines and split lines to pickings
[sale_order_line_configurator](sale_order_line_configurator/) | 14.0.1.0.1 |  | Adds a product configurator on sale order line
[sale_order_line_copy](sale_order_line_copy/) | 14.0.1.2.1 |  | Duplicate single order lines or sections on sale order
[sale_order_line_decription_to_stock_move](sale_order_line_decription_to_stock_move/) | 14.0.1.0.0 |  | SO line description to Stock move
[sale_order_line_delivery_date_change_scheduled_date](sale_order_line_delivery_date_change_scheduled_date/) | 14.0.1.0.4 |  | Change Scheduled Date with Delivery Time
[sale_order_line_delivery_time](sale_order_line_delivery_time/) | 14.0.1.0.0 |  | Sale Order Line Delivery Time
[sale_order_line_description_without_product](sale_order_line_description_without_product/) | 14.0.1.0.0 |  | Remove product and product code from default description
[sale_order_line_invoice_date](sale_order_line_invoice_date/) | 14.0.1.0.0 |  | Sale Order Line Invoice Date
[sale_order_line_limit](sale_order_line_limit/) | 14.0.1.0.3 |  | Sale Order Line Limit
[sale_order_line_open_form](sale_order_line_open_form/) | 14.0.1.0.0 |  | Open Form view from sale order's line
[sale_order_line_qty_available](sale_order_line_qty_available/) | 14.0.1.0.0 |  | Add qty_available to sale order line
[sale_order_line_stock_pickings](sale_order_line_stock_pickings/) | 14.0.1.0.0 |  | Show deliveries (stock pickings) on sale order lines
[sale_order_line_view](sale_order_line_view/) | 14.0.1.0.2 |  | Add a readonly SO line view for viewing SO line specific info
[sale_order_line_view_analytic_tags](sale_order_line_view_analytic_tags/) | 14.0.1.0.0 |  | Use Analytic tags in search, grouping and tree view
[sale_order_line_view_team_filter](sale_order_line_view_team_filter/) | 14.0.1.0.0 |  | Use Sales team filter in sale order line tree view
[sale_order_lock_on_invoiced](sale_order_lock_on_invoiced/) | 14.0.1.0.0 |  | Lock sale order after it state is fully invoiced
[sale_order_mass_cancel](sale_order_mass_cancel/) | 14.0.1.0.0 |  | Enables cancelling multiple sales at once
[sale_order_mass_confirm](sale_order_mass_confirm/) | 14.0.1.0.0 |  | Enables confirming multiple sales at once
[sale_order_membership_attachment](sale_order_membership_attachment/) | 14.0.1.1.1 |  | Enables sending product attachments with order confirmation email wizard
[sale_order_multi_company_rule_only_own_company](sale_order_multi_company_rule_only_own_company/) | 14.0.1.0.0 |  | Shown own company Orders only
[sale_order_my_orders_no_default_filter](sale_order_my_orders_no_default_filter/) | 14.0.1.0.0 |  | Remove My order-default filter
[sale_order_name_salesperson_notice_period_to_note](sale_order_name_salesperson_notice_period_to_note/) | 14.0.1.0.2 |  | Add sale order name to sale order note on order confirm
[sale_order_no_autofollow](sale_order_no_autofollow/) | 14.0.1.0.1 |  | Don't set customer as a SO follower automatically
[sale_order_no_open_form](sale_order_no_open_form/) | 14.0.1.0.0 |  | This module prevents to open forms on specified fields.
[sale_order_note_by_comment_to_picking](sale_order_note_by_comment_to_picking/) | 14.0.1.0.1 |  | 'Note by' comment to picking of a salesperson
[sale_order_note_to_invoice](sale_order_note_to_invoice/) | 14.0.1.0.1 |  | Move SO line notes to invoice
[sale_order_order_lines_analytic_account_required](sale_order_order_lines_analytic_account_required/) | 14.0.1.0.0 |  | Required Analytic Account for Sale Order Orderlines
[sale_order_partner_clause_to_note](sale_order_partner_clause_to_note/) | 14.0.1.0.0 |  | Sale Order - add Sale clause to note field
[sale_order_partner_contact_only](sale_order_partner_contact_only/) | 14.0.1.0.0 |  | Don't show other address types in SO partner select
[sale_order_partner_delivery_method](sale_order_partner_delivery_method/) | 14.0.1.0.0 |  | Delivery method is assigned based on partner's delivery method
[sale_order_partner_disable_onchange](sale_order_partner_disable_onchange/) | 14.0.1.0.0 |  | Disable partner (customer) onchange on sale
[sale_order_partner_disable_onchange_for_delivery_address](sale_order_partner_disable_onchange_for_delivery_address/) | 14.0.1.0.0 |  | Disable partner (customer) onchange on sale for Delivery address
[sale_order_partner_onchange_suggest_partner_itself](sale_order_partner_onchange_suggest_partner_itself/) | 14.0.1.0.0 |  | Suggest customer itself instead of its sub-addresses
[sale_order_partner_strict_with_partner_itself](sale_order_partner_strict_with_partner_itself/) | 14.0.1.0.0 |  | Allow customer itself or correct type and parent for address
[sale_order_partner_tag_to_crm_tag](sale_order_partner_tag_to_crm_tag/) | 14.0.1.0.0 |  | Tag from partner category to sale order CRM tag
[sale_order_pricelist_no_copy](sale_order_pricelist_no_copy/) | 14.0.1.0.0 |  | Do not copy pricelist when copying sale order
[sale_order_pricelist_price_by_categ_qty](sale_order_pricelist_price_by_categ_qty/) | 14.0.1.0.0 |  | Set sale order line price by pricelist quantities
[sale_order_product_label](sale_order_product_label/) | 14.0.1.0.0 |  | Sale Order Product Label
[sale_order_proforma_country_group_text](sale_order_proforma_country_group_text/) | 14.0.1.0.0 |  | Get report text from country groups setting
[sale_order_project_in_header](sale_order_project_in_header/) | 14.0.1.0.1 |  | Moves analytic account to SO header and sets it as required
[sale_order_promised_delivery_range](sale_order_promised_delivery_range/) | 14.0.1.0.1 |  | Adds new fields for storing date range of promised delivery
[sale_order_promised_delivery_range_in_list](sale_order_promised_delivery_range_in_list/) | 14.0.1.0.0 |  | Makes the sale order list show promised delivery range
[sale_order_requested_delivery_date](sale_order_requested_delivery_date/) | 14.0.1.0.1 |  | Adds a new field for storing date of requested delivery
[sale_order_route_in_header](sale_order_route_in_header/) | 14.0.1.0.0 |  | Allows editing route for all SO lines at once
[sale_order_sale_type](sale_order_sale_type/) | 14.0.1.0.1 |  | Sale Type field is added to sales
[sale_order_send_all_documents_by_email](sale_order_send_all_documents_by_email/) | 14.0.1.0.1 |  | Sales - Send sale, invoice and pickings prints if possible
[sale_order_show_addresses](sale_order_show_addresses/) | 14.0.1.0.0 |  | Show the addresses below their fields
[sale_order_show_purchase_order](sale_order_show_purchase_order/) | 14.0.1.0.0 |  | Show Linked Purchase Orders on Sale Orders
[sale_order_show_reporting_group](sale_order_show_reporting_group/) | 14.0.1.0.0 |  | Show 'Reporting' group in SO form without belonging to the Technical group
[sale_order_stock_location_partner](sale_order_stock_location_partner/) | 14.0.1.0.0 |  | Auto-create stock locations for partners from sale order
[sale_order_stock_picking_auto_return](sale_order_stock_picking_auto_return/) | 14.0.1.0.0 |  | Ask to return delivered products when cancelling a sale
[sale_order_subtotal_values](sale_order_subtotal_values/) | 14.0.1.0.0 |  | Recompute Sale Order line subtotal values
[sale_order_tax_required](sale_order_tax_required/) | 14.0.1.0.0 |  | Tax is required on all Sale Order lines
[sale_order_tree_customer_reference](sale_order_tree_customer_reference/) | 14.0.1.0.0 |  | Add customer reference to sale order tree view
[sale_order_tree_untaxed](sale_order_tree_untaxed/) | 14.0.1.0.0 |  | Show untaxed amount in sale order tree
[sale_order_tree_view_quotations_only](sale_order_tree_view_quotations_only/) | 14.0.1.0.0 |  | Sale Quotations tree view - Show only quotations
[sale_order_unlock](sale_order_unlock/) | 14.0.1.0.0 |  | Allows unlocking locked sale orders for managers
[sale_order_warehouse_do_not_copy](sale_order_warehouse_do_not_copy/) | 14.0.1.0.0 |  | Do not copy a warehouse when copying a sale order
[sale_order_warranty](sale_order_warranty/) | 14.0.1.0.1 |  | Sale Order Warranty
[sale_order_week_of_shipment](sale_order_week_of_shipment/) | 14.0.1.0.1 |  | Week of shipment field to sale order
[sale_order_year_of_shipment](sale_order_year_of_shipment/) | 14.0.1.0.0 |  | Sale Order year from commitment date
[sale_partner_default_note](sale_partner_default_note/) | 14.0.1.0.0 |  | Add a default sale note (terms and conditions) for partner
[sale_payment_acquirer_optional_so_reference](sale_payment_acquirer_optional_so_reference/) | 14.0.1.0.0 |  | Adds an option to not create a payment reference for SO
[sale_quotation_list_customer_order_number](sale_quotation_list_customer_order_number/) | 14.0.1.0.0 |  | Adds customer order number to sale quotation list view
[sale_stock_availability_unreserved](sale_stock_availability_unreserved/) | 14.0.1.0.1 |  | Add product unreserved availability to SO line
[sale_stock_client_ref_to_picking](sale_stock_client_ref_to_picking/) | 14.0.1.0.0 |  | Move SO customer reference to created stock pickings
[sale_stock_disable_warehouse_onchange](sale_stock_disable_warehouse_onchange/) | 14.0.1.0.0 |  | Don't auto-change company when warehouse changes

[//]: # (end addons)
