.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
Sale Order: Membership Product Attachments in Emails
====================================================

This module extends OCA's mail_attach_existing_attachment to carry
attachments from membership products to sale orders, and from there to
the order's e-mail wizard.

When a sale order with a membership product is confirmed, any
attachments on that product are copied to the sale order. When the
order confirmation e-mail wizard is opened afterwards, those
attachments are pre-selected automatically.

Configuration
=============

#. By default, all attachments are pre-selected in the wizard. To
   require the user to check them manually instead, create a config
   parameter named
   ``sale_order_membership_attachment.bypass_attachment_autoselection``
   with the value ``False``.

Usage
=====

#. Add an attachment to a membership product's new attachments field.
#. Create and confirm a sale order that sells that product - the
   attachment is copied to the sale order.
#. Send an email via the sale order's email wizard - the membership
   product attachment is automatically added and shown.

Known issues / Roadmap
======================
* Only works when sending order confirmations via the mail wizard, not
  with automated confirmation emails.
* All of a sale order's attachments are shown and selectable in the
  wizard, not only the ones copied from membership products.

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
