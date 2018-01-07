
.. _drideos:

========
DrideOS
========

DrideOS is a specific customization of Raspbian_ "Jessie".  This is a Debian Linux 
deriviative hosting common features you would find on any Linux computer.

It is important to note that while the operating system is not *embedded* by nature, 
the configuration sports a minimal interface type commonly referred to as *headless*.

.. note::
    There is no desktop/GUI support provided for this device type.

The system :ref:`architecture` involves specific kernel modules, daemons, 
RESTful API and watchdogs to ensure an always available system with 
access from a remote device.

Support is included for these common programming languages/platforms:

* Python 2.7

* Node JS v8.9.0


Intent
------

The goal of DrideOS is to build a modular architecture such that developers may
exchange different parts where interested and not have to re-create the entire
system from scratch.

You can for example replace the implementation on how video is captured and recorded
when the hardware button is pressed without breaking the mobile application or cloud 
storage of your uploaded videos.

    *"Build the best dashcam in your car from an Open Source community."
    - Yossi Neiman*

.. _raspbian: https://www.raspberrypi.org/downloads/raspbian/


DrideOS Source
--------------

You can obtain the source code to create the DrideOS here:

https://github.com/dride/drideOS-image-generator


Kernel modules
--------------

.. todo::
    Obtain information/specifics on kernel modules from maintainer of DrideOS image
