.. _architecture:

===================================
Dride Architecture
===================================

Raspbian_ has been customized for specific use and named :ref:`drideos`. 
The system architecture involves specific kernel modules, daemons, 
RESTful API and watchdogs [#]_ to ensure an always available system with
access from a remote device.


Services/Daemons
================

There are currently two services enabled:

* /etc/init.d/dride-core
* /etc/init.d/dride-ws

Webservices API
===============

Currently in this version

* dride-ws - Providing the web services outlined here: :ref:`api`


Cron
====
Currently all cron jobs are organized under user **root**.  There is currently
one cron job that runs every minute.

Clean up diskspace removing oldest videos::

    $> sudo crontab -l
    * * * * * node /home/Cardigan/modules/video/helpers/cleaner.js



Startup Sequence
================

Following normal system startup procedures boot, kernel modules, etc. DrideOS
initiates the start of the two services.

dride-core
----------

1. Welcome LED
2. Decode Clips
3. Start recording
4. Bluetooth

dride-ws
----------

1. Start :ref:`api`


Monitoring/Performance
======================

.. todo::

    Future enhancement

.. _raspbian: https://www.raspberrypi.org/downloads/raspbian/

.. [#] Watchdogs are a *future* enhancement
