.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Sale Order line configurator
============================

Adds a product configurator workflow directly on the sale order lines

Known issues / Roadmap
======================

When both columns are visible, the line description is rendered in both cells.

Changelog
=========
* Migration from v17 to v19
   * Added a JS code to bypass the cores new addition, that prevented 
   the product and product variant columns being available at the same time. 
   This is done gracefully, so that future changes to the core code should 
   not break this module, but also allow the core changes.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekaläinen@tawasta.fi>
* Joonas Lahtinen <joonas.lahtinen@futura.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy