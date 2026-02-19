.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
Sale: never auto-update SOL description
=======================================
This module prevents Odoo from automatically regenerating the sales order line
description (field ``name``) when the product is set or changed. The existing
value in ``name`` is kept as-is, allowing manual or custom descriptions to
remain untouched.

Installation
============

* Just install this module

Configuration
=============
\-

Usage
=====

* Create or edit a Sales Order.
* Add a product on a sales order line.
* The module will not overwrite the existing line description (``name``).
  This allows you to keep a manual/custom description even when selecting
  products or changing variants.

Known issues / Roadmap
======================
* None

Credits
=======

Contributors
------------
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
