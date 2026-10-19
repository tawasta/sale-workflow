.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Sale Warnings
=============

* Adds options to how Sale Warnings are shown

  * Warning

    * Show the warning in the banner at the top of the sales order only

  * Popup Warning

    * Show popup warning in addition to the banner

  * Blocking Warning

    * Prevent changing the customer of an existing sales order to this
      customer. The banner is not shown.

* The popup and the blocking are provided by the module partner_warnings
  (abstract model ``partner.warning.mixin``), which is also used by other
  documents, e.g. stock_warnings
* Currently adds warnings to fields

  * partner_id

Configuration
=============
\-

Usage
=====

* User

  * Install module
  * Go to Settings -> Sale

    * Check "Sale Warnings"

* Developer

  * To add the same warnings to another document, see the Usage section of
    partner_warnings

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Joona Isoaho <joona.isoaho@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
