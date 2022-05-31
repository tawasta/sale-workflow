.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
Set sale order line price by pricelist quantities
=================================================

Compute a sale order line price by pricelist quantities. Product categories that
have use_on_discount-field ticked will be used in computation.

An example below.

Categories A and B have use_on_discount-field ticked.

Sale Order lines:
line: 1, product: A, category: A, quantity: 3, price: 0,
line: 2, product: B, category: A, quantity: 2, price: 0,
line: 3, product: C, category: B, quantity: 4, price: 0,

Pricelist X:
item: 1, product: A, category: A, quantity: 5, price: 10,
item: 2, product: B, category: A, quantity: 3, price: 6,
item: 3, product: C, category: B, quantity: 3, price: 25,
item: 4, product: C, category: B, quantity: 5, price: 32,

So after pressing Global discount button the same Sale order lines prices are:

Sale Order lines:
line: 1, product: A, category: A, quantity: 3, price: 10,
line: 2, product: B, category: A, quantity: 2, price: 6,
line: 3, product: C, category: B, quantity: 4, price: 25,

This means that products A and B prices were calculated as there were
5 of them per Sale order line, because they belong to the same category.
Product C's price became 25 because there were more than 3 of it on the Sale
order line and item 3 price was picked.

Configuration
=============
\-

Usage
=====
Use Compute global discount-button to compute units prices according to
Sale order's pricelist quantities

Known issues / Roadmap
======================
\-

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
