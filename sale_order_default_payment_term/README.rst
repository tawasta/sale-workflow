.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================================
Set a default payment term for sales if a partner does not have one
===================================================================

This module was created to have a fallback payment term for sales
if a partner does not have a payment term set.

Configuration
=============
None needed

Usage
=====
Go to Sales settings and select the payment term to be used as default.
Then create a sale in which a partner does not have a payment term set.
The payment term defined in the Sales settings should appear on the sale.

Known issues / Roadmap
======================
The module modifies _compute_payment_term_id -function.
Other modules might modifies this function too and change its
behaviour.

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
