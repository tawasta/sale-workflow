.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================
Sale Order - Commitment Date Automation
=========================================

This module automatically fills the delivery date (``commitment_date`` field)
on a sale order when the order is confirmed. The calculation can be configured
either company-wide or per sales team. Does not override manually set delivery dates. 
Weekends are skipped in the calculation, however holidays are not taken into account.

Configuration
=============

Go to *Sales › Configuration › Settings* and find the *Delivery date
automation* setting.

Choose the automation mode:

* **No automation** — delivery date is not filled automatically.
* **Company-wide** — the same calculation is used for every order.
* **Sales team specific** — each sales team can have its own delay.

For company-wide or team mode, configure:

* **Timezone** — the timezone used when evaluating the confirmation time.
* **Time cutoff** — confirmation before this time counts the current day as day 0;
  confirmation at or after this time counts the current day as day 1.
* **Default delivery lead time (weekdays)** — number of weekdays to add.

When *Sales team specific* mode is active, the number of weekdays can be set on
each sales team under *Sales › Configuration › Sales Teams*. Teams with no own
value fall back to the company default.

Usage
=====

Confirm a sale order. If the delivery date is empty and automation is enabled,
it is automatically calculated and filled into the ``commitment_date`` field.

Known issues / Roadmap
======================


Credits
=======

Contributors
------------

* Joonas Lahtinen <joonas.lahtinen@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
