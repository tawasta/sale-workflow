.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================================
Disable adding analytic account info from SO header to invoice lines
====================================================================

When creating an invoice from a sale order the analytic account information
is inherited to invoice lines. This module prevents this functionality and
invoice lines get their analytic distribution information only from their
respective sale order lines.

Configuration
=============
There is no need to configure anything

Usage
=====
Go to a sale order that has an analytic account set to its header. Then
create an invoice from that sale order. The invoice lines will not have
analytic distribution inherited from sale order header.

Known issues / Roadmap
======================
This module has sale_order_project_in_header module in its dependencies so
that Analytic Account is shown on sale order form. This is not required, but
it better shows what Analytic Account is used on a sale order.

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
