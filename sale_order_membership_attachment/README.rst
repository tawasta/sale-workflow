.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
Sale Order: Membership Product Attachments in Emails
====================================================

* Extends the functionality of OCA's mail_attach_existing_attachments to bring
  attachments from membership products to sale orders, and from there to the 
  SO e-mail wizard.

Configuration
=============
* By default all of the attachments are selected by default in the wizard. If
  you prefer the user to manually check the relevant ones instead, create a new
  config parameter "sale_order_membership_attachment.bypass_attachment_autoselection"
  with the value False.

Usage
=====
* Add a membership product attachment into the new field of a Membership Product
* Create a Sale Order where that product is sold.
* Confirm the Sale Order, and the attachment gets carried over to the Sale Order's attachments
* Send an email via Odoo's SO email wizard, and the membership product attachment is 
  automatically added and shown in the wizard
* Note: be aware that any and all attachments from SO will be added and shown in the wizard,
  also those not related to membership products

Known issues / Roadmap
======================
* Currently only works when sending order confirmations via Odoo's mail wizard, not with automated
  confirmation emails

Credits
=======

Contributors
------------
* Valtteri Lattu <valtteri.lattu@tawasta.fi>
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
