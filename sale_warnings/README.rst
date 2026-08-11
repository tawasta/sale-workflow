.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============
Sale Warnings
=============

* Adds options to how Sale Warnings are shown

  * Warning

    * Show underneath the field only

  * Popup Warning

    * Show popup warning in addition to underneath the field

  * Blocking Warning

    * Show popup warning and prevent choosing the value

* Allows easy extension to other Many2One fields
* Currently adds warnings to fields:

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

    * Add sale_warn_msg and sale_warn_level to target model similar to models/partner.py

        * res.partner already has sale_warn_msg field from other module
        * Add the field name to "Currently adds warnings to field list" above

    * Add sale_order field name and model of which the fields points to into
      models/sale_order.py check dictionary
    * Add view similar to views/res_partner.xml

        * res.partner already has field for sale_warn_msg

    * Add the widget into sale order field attributes in views/sale_order.xml

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Joona Isoaho <joona.isoaho@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
