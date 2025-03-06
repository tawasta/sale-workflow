.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================================
Analytic distribution is required in SO lines when invoicing an order
=====================================================================

Creating an invoice from SO is not possible if analytic distributions are not
set on lines.  A message is shown if analytic distributions are missing when
trying to make a new invoice.

Configuration
=============

Usage
=====
Go to a sale order and try to make an invoice when analytic distributions are
missing on order's lines. A message is shown in this case. This can be bypassed
by creating sale_bypass_analytic_distribution_required system parameter.  Its
value can be set to True or 1.

Known issues / Roadmap
======================

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
