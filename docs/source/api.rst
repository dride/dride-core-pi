.. _api:

===
API
===

The Dride webservices are one such component that provides a predefined
interface for other devices to get/set device information.

Routes
======

+---------------------------+------+---------------------------+
| URL                       | VERB | Purpose                   |
+===========================+======+===========================+
| ``/api/getClips``         | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/getSettings``      | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/deleteClip``       | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/deleteAllClips``   | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/updateFirmware``   | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/isOnline``         | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/getSerialNumber``  | GET  | A list of all video clips |
+---------------------------+------+---------------------------+
| ``/api/indicator``        | GET  | A list of all video clips |
+---------------------------+------+---------------------------+



Static Routes
=============

Static routes offer access to the media: thumbnails and video's for each
clip.

Examples:

* /modules/video/thumb/1515036499325.jpg
* /modules/video/clip/1514850857979.mp4


Accessing the API
=================

First establish connection with your development workstation via WiFi.

An Example:

Call port 9000, **GET** verb::

    http://192.168.42.1:9000/api/getSerialNumber

A **curl** example::

    curl http://raspberrypi.local:9000/api/getSerialNumber

And output::

    {"serial":"00000000445acdb3"}
