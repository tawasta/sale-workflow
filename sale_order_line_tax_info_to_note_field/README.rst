.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Sale Order: Tax Info on SO Note
===============================

* Taxes get a new sale_order_note field
* When a Sale is confirmed, the Sale Order lines' taxes are checked
  and text from their sale_order_note fields is fetched into SO's 
  Notes field if such text exists.
* This module also deletes order's previous sale_order_note field
  text if the order has been cancelled and confirmed again.

Configuration
=============
* Add the the Sale Order Notes texts to relevant taxes

Usage
=====
* Install the module by going to Apps and click 'Install'.

Known issues / Roadmap
======================
* There are no known issues with this module.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
