.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Manufacturing Status for Sale Orders
====================================

Shows the status of Manufacturing Orders for Sale Orders as follows:

* Nothing to Manufacture: no Manufacturing Orders originated from the Sale Order
* Manufacturing Exception: some MOs are in Cancel state
* Fully Manufactured: all MOs are in Done state
* To Manufacture: some MOs are unfinished

The status is fetched by comparing the procurement groups of the Manufacturing Order and the Sale Order

Info about individual Manufacturing Orders is shown in the Sale Order form

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
* Fine-tuning access rights based on which user groups (salesmen, workers...) should see what

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
