
.. _hacking:

=======
Hacking
=======

This page contains some useful information to get you started


Enable SSH over USB
-------------------

You can plug your USB cable from your development computer into the **USB**
port of the device.  This is **not** the same USB port accessible via the device.

Benefits:

* Directly SSH into your Dride, example: ``ssh pi@raspberrypi.local``
* Your Dride may access the internet via the host development PC

.. note::
    This requires disassembly of the :ref:`dridezero`.

Edit this the file ``/boot/config.txt``::

    dtoverlay=dwc2


Next edit and save this file ``/boot/cmdline.txt``::

    modules-load=dwc2,g_ether

It **MUST** be added *after* the ``rootwait`` as shown here::

    dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=b62737d7-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait modules-load=dwc2,g_ether

.. warning::
    You must not include extra spaces, or new line characters. Failure to do this
    wrong **may** prevent your device from booting.

If your device fails to boot due to an issue caused by editing these files - simply
remove the card and rewrite the Dride OS image.


Install your public SSH key
---------------------------

Install your public SSH key to allow you to more easily remotely connect via SSH::

    ssh-copy-id -i ~/.ssh/id_rsa.pub pi@raspberrypi.local

