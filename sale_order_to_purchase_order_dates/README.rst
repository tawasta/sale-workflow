.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Sale Order to Purchase Order - Date Extension
=============================================

* Looks at 1) the requested delivery date given by the end customer of a sale
  order and 2) the usual delivery delay of the vendor that is dropshipping the 
  goods to them. 
* When creating a purchase order from the sale, the delay information is used
  to compensate and suggest an earlier requested delivery date from the
  vendor.
* Intended for situations where vendors are known to often dropship goods
  late, so that there is a buffer between the requested delivery and the 
  actual date when end customer needs the goods.

Configuration
=============
* Go to the vendor form and fill in the new "Delivery delay to end customer"
  field

Usage
=====
* Click the "Create RFQ" button on the Sale Order form. Select a vendor and 
  edit the Requested delivery date field if necessary. Print a purchase order.

Known issues / Roadmap
======================
\-

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
