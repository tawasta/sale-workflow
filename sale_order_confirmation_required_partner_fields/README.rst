.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Mandatory Partner Field Check Upon SO Confirmation
==================================================

* Allows configuring a list of partner fields that must be filled for the
  customer before a sale order can be confirmed

Configuration
=============
* Set the mandatory customer fields in Sales -> Configuration

Usage
=====
* Create and confirm a Sale Order as usual. If mandatory fields are empty, 
  an error message is shown

Known issues / Roadmap
======================
* Currently set as uninstallable: the module works, but safety limitations
  in Odoo core prevent editing the m2m field connections to ir.models.fields
  so reconfiguring the required fields always raises an exception. The
  module still works as long as you configure the fields in one go, and
  if there is need for reconfiguration, you re-install the whole module.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
