.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================================
Sale Orders – Force to always use Customer as the Delivery Address
==================================================================

::

    The module forces to always use Customer as the Delivery Address on Sale Orders.
    The _compute_partner_shipping_id method is overrun to enable this behaviour and
    it works without conditions. This is a rare need, so take note of that.

Configuration
=============
::

    None is necessary

Usage
=====
::

    Go to Apps to install the module. Then create a sale order and notice
    that the delivery address will always be the same as the customer.

Known issues / Roadmap
======================
::

    Use this module only when really needed.

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
