.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Finalization state for Sale Orders
==================================

 * Adds a new state, 'Finalization', between Quotation Sent and Sale Order, where the Sale Order document is still editable
 * Intended for situations where the Quotations need changes before they get converted to Sale Orders (e.g. the customer approves the quote but with slight changes)

Installation
============
* If the Odoo installation uses both Sales Management and Warehouse Management, you should also install sale_order_finalization_state_stock. It adds the proper state-based readonly attributes to those Sale Order fields provided by core's sale_stock module.

Configuration
=============
* No configuration needed

Usage
=====
\- 

Known issues / Roadmap
======================
* This module should currently not be used together with other modules that modify the states of the Sale Order. To have the Finalization state appear in the correct position between Quotation Sent and Sale Order, the whole state list is redefined instead of using selection_add.

Credits
=======

Contributors
------------
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
