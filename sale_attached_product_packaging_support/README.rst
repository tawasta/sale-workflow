.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
Sale Order: Attached products packaging support
================================================
* Extends ``sale_attached_product``: attached lines get the main line's unit
  (e.g. 6-pack) when the attached product allows it (its own unit or one of
  its Packagings), and are priced in that unit
* Otherwise the attached line keeps its own unit with the same quantity, as
  in ``sale_attached_product``

Configuration
=============
* Add the packaging (e.g. 6-pack) to the attached product's Packagings
* To follow later unit changes of the main line, set the system parameter
  ``sale_attached_product.auto_update_attached_lines``

Usage
=====
* Sell the main product as e.g. 1 x 6-pack: the attached line is also added 
  as 1 x 6-pack
* Unit changes are followed only on quotations, not on confirmed orders

Known issues / Roadmap
======================
* Note that ``sale_attached_product`` is not yet officially for 19.0 and a 
  placehodler version currently resides only in Futural ``oca-backports``
  repo.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
