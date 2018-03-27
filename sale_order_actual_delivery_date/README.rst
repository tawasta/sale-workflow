.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Sale Order Actual Delivery Date
===============================

* Adds a new field to Sale Orders for storing the actual delivery date

Configuration
=============
* No configuration needed

Usage
=====
* Create a Sale Order and deliver the products. When delivered quantity >= 
  sold quantity for all non-service lines, the date gets set.

Known issues / Roadmap
======================
* Note: the module does not take into account any possible product returns and
  subsequent re-deliveries.

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
