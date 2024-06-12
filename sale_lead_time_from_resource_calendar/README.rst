.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Sale: Lead Time Based on Resource Calendar
==========================================

* Takes into account weekends and global time off in Sale Order Line 
  lead time calculation, by adding extra days to the lead time if the 
  timeframe spans over weekends or global days off.

Configuration
=============
* Configure a resource calendar via Employees -> Working times, and set e.g.
  weekends to not be working days
* In the resource calendar, optionally also add Global Time Off days for e.g. 
  christmas holidays. 

  * Note: have the Start Dates start from 00:00:00 and End Dates end in
    23:59:59 to ensure the calculations work

* Go to Sales -> Configuration -> Settings and select the configured 
  resource calendar in "Resource Calendar for Calculating Sale Lead Times".

Usage
=====
* Create a Sale Order and add a line with a product that has a Customer
  Lead Time defined.
* The Lead Time of the SO Line will take into account the weekends
  and global times of the resource calendar.
* When you add multiple lines, the Sale Order's Expected Delivery Date
  will be based on either the shortest or the longest lead time on the 
  SO lines, depending on the selected Shipping Policy on the SO.

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

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
