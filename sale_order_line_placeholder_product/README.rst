.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================================
Prevent Quotation To Sale Order For The Code
============================================

This module adds a boolean field for the product form. When this field is checked, a quotation 
that includes this product cannot be confirmed to a sale order. Also this product's description 
is added to the selected product's description on the same sale order line. 

The original product has to have this custom field checked and the targeted sale order has to be 
saved before changing the product for this module to work properly. After this, all the other 
products will inherit this product's description. 

Other products that do not have this boolean field checked, will show the product's name on sale 
order lines description field only if the product has Description for Quotations as an empty 
field. Else the Description for Quotations is shown in sale order line description field. 

Configuration
=============
\-

Usage
=====
\-

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
