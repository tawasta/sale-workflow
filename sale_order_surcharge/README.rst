.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Sale Order Surcharges
=====================

Adds an option to define a surcharge that will be added to selected partners'
Sale Orders automatically

Configuration
=============
* Define the surcharge product and percentage to be used in Sales -> 
  Configuration -> Settings
* Check the "Apply surcharge" box for the customers of your choice

Usage
=====
* Create a new Sale Order and select a customer with surcharging enabled
* Confirm the order, and a new SO line gets added automatically with the
  selected surcharge product. The price is the selected percentage of the
  untaxed SO total amount.

Known issues / Roadmap
======================
* Note: in multicompany environments both companies can define their own
  surcharge products, but currently it is not possible to have a customer
  that one company applies a surcharge to, and another company does not.

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
