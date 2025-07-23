.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================================
Insert PDF attachment to a sale order to include it in its PDF Quote print
==========================================================================

Add a PDF header document or/and a PDF footer document to sale order. These documents
are added to the PDF quote print of the sale order.

A function checks that documents are of PDF type.

Configuration
=============
No configuration is needed

Usage
=====
Go to a sale order and add a PDF header document and a PDF footer document to it and print
the quotation of the sale order.

Known issues / Roadmap
======================
This module inherits _render_qweb_pdf_prepare_streams -function of ir.actions.report model.

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
