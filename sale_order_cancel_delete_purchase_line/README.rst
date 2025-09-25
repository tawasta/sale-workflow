.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
Delete purchase lines when a sale order is cancelled
====================================================

Use this module with caution!

It is advicable, but not required, to use purchase_order_merge_by_sale_order
module to have purchases linked to a specific sale order. Then deleted purchase
lines only affects one sale order.

Purchase lines are deleted no matter in what state a purchase order is.
Purchase orders are also set to draft by first cancelling them.

Configuration
=============
Have MTO and Buy route combination enabled to create purchases from
sales.

Usage
=====
Install the module and test it by cancelling a sale order which has
purchase orders linked to it.

Known issues / Roadmap
======================
Deleting removes purchase line information, but it can be created again
by confirming a sale order that was previously cancelled.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
