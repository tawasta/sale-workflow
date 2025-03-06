.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=====================================================
Sale Order: 'Online payment' field SO duplication fix
=====================================================

* Forces the re-calculation of Sale Order's require_payment boolean field 
  when copying an SO. 
* In core, when the field is computed to true, quotation e-mails will contain 
  a button with "Accept and pay" text instead of simply "View quotation". This
  could cause wrong texts to show up in copied Sale orders' quotation e-mails.

Configuration
=============
* None needed

Usage
=====
* Just copy a Sale Order

Known issues / Roadmap
======================
\-

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
