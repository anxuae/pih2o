
.. image:: https://raw.githubusercontent.com/anxuae/piH2O/master/templates/pih2o.png
   :align: center
   :alt: PiH2O


The ``pih2o`` project attempts to provide an automatic flower watering application *out-of-the-box*
in pure Python for Raspberry Pi.

Requirements
------------

The requirements listed below are the one used for the development of ``pih2o``, but other
configuration may work fine. The **pump** can be replaced by an electro valve if the tank
water is upper than the flowers (watering by gravity).

Hardware
^^^^^^^^

* 1 Raspberry Pi 2 Model B (or higher)
* 1 Peristaltic dosing pump (or electro valve)
* 5 soil moisture sensors for Arduino TE215
* 1 Analog-to-Digital Converter (ADS1115 16 Bit 16 Byte 4 Channel I2C)

Software
^^^^^^^^

* Python ``3.5.3``
* RPi.GPIO ``0.6.3``

Install
-------

A brief description on how to set-up a Raspberry Pi to use this software.

1. Download latest Raspbian image and set-up an SD-card. You can follow
   `these instructions <https://www.raspberrypi.org/documentation/installation/installing-images/README.md>`_ .

2. Insert the SD-card into the Raspberry Pi and fire it up. Use the raspi-config tool that is shown
   automatically on the first boot to configure your system (e.g., expand partition, change hostname,
   password, enable SSH, configure to boot into GUI, etc.).

   .. hint:: Don't forget to enable the I2C in raspi-config.

3. Reboot and open a terminal. Install the latest firmware version:

   ::

        $ sudo rpi-update

4. Upgrade all installed software:

   ::

        $ sudo apt-get update
        $ sudo apt-get upgrade

5. Install ``pih2o`` from the `pypi repository <https://pypi.org/project/pih2o/>`_:

   ::

        $ sudo pip3 install pih2o

Run
---

Start the automatic flower watering application using the command::

    $ pih2o

Run a developing version
------------------------

If you want to use an unofficial version of the ``pih2o`` application, you need to work from a
clone of this ``git`` repository. Replace the step 5. of the `Install`_ procedure above by the
following actions:

- clone from github ::

   $ git clone https://github.com/anxuae/piH2O.git

- go in the cloned directory ::

   $ cd piH2O

- run ``pih2o`` with the command ::

   $ PYTHONPATH=. python3 pih2o/h2o.py

Configuration
-------------

At the first run, a configuration file is generated in ``~/.config/pih2o/pih2o.cfg``
which permits to configure the behavior of the application. The configuration can be
easily edited using the command::

    $ pih2o --config

The default configuration can be restored with the command (strongly recommended when
upgrading ``pih2o``)::

    $ pih2o --reset

Below is the default configuration file:

.. code-block:: ini

    [GENERAL]
    # Start pih2o at Raspberry Pi startup
    autostart = True


Circuit diagram
---------------

.. image:: https://raw.githubusercontent.com/anxuae/piH2O/master/templates/sketch.png
   :align: center
   :alt: Electronic sketch
