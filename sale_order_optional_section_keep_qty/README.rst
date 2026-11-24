.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
Sale Order Optional Section Keep Quantity
=========================================

* Changes the optional sections of quotations: setting a section optional no
  longer sets the quantities of its products to 0.
* The optional sections of quotation templates also keep their quantities, so
  that the quotations created from a template show them.
* The products, quantities and section total of an optional section are shown
  on the quotation, but they are not included in the quotation total.
* The margin and margin percentage of each line and the section total are shown
  as on regular sections. The order margin leaves the optional lines out, as
  the total does.
* The quotation print and the customer portal mark the section as optional and
  not included in the total.
* Delivery, discount and down payment lines are always included in the total,
  also when they are added after an optional section.
* The global discount of the quotation is computed without the optional lines.
* A quotation with an optional section cannot be confirmed. When the customer
  chooses the optional section, the salesperson unsets the optional section so
  that it becomes a regular one; otherwise the salesperson deletes the section.
  Accepting the quotation in the portal tells that the salesperson first
  handles the optional sections.
* The customer cannot change the quantities of the optional products in the
  portal.

Configuration
=============
\-

Usage
=====
* Open a quotation and the menu of a section on the order lines.
* Choose "Set Optional". "Unset Optional" makes it a regular section again.
* A section can be set optional only on a quotation, not on a confirmed order.

Known issues / Roadmap
======================
* The sales analysis report sums all lines of a quotation, optional lines
  included.

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
