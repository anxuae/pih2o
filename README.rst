
.. image:: https://raw.githubusercontent.com/anxuae/piH2O/master/templates/pih2o.png
   :align: center
   :alt: PiH2O


The ``pih2o`` project attempts to provide an automatic plant watering application *out-of-the-box*
in pure Python for Raspberry Pi.

Requirements
------------

The requirements listed below are the one used for the development of ``pih2o``, but other
configuration may work fine. The **pump** can be replaced by an electro valve if the tank
water is upper than the plants (watering by gravity). The number of **soil moisture sensors**
can be easily adapted from 1 to 4.

Hardware
^^^^^^^^

* 1 Raspberry Pi 2 Model B (or higher)
* 1 Peristaltic dosing pump (or electro valve)
* 1 to 4 soil moisture sensors (Arduino TE215)
* 1 Analog-to-Digital Converter (ADS1115 16 Bit 4 Channel I2C)
* 1 Relay module (5V DC)

Software
^^^^^^^^

* Python ``3.5.3``
* RPi.GPIO ``0.6.3``
* adafruit-ads1x15 ``1.0.2``
* croniter ``0.3.23``
* blinker ``1.4``
* flask ``1.0.2``
* flask-restful ``0.3.6``
* flask-sqlalchemy ``2.3.2``

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

Start the automatic plant watering application using the command::

    $ pih2o

The application acts as a daemon running on the Raspberry Pi. It can be controlled thanks
to an `RESTful API <https://github.com/anxuae/pih2o/blob/master/docs/api.rst>`_.

The ``pih2o`` is scheduled to wake up every given interval, power the soil moisture
sensors and take humidity measurement (or threshold if no analog input available).
Finally the sensors are powered off to extend their lifespan.

Define the record interval
^^^^^^^^^^^^^^^^^^^^^^^^^^

The record interval (i.e. time between each humidity measurement) is defined
in the `Configuration`_ using the `crontab syntax <https://fr.wikipedia.org/wiki/Cron>`_
which is summarized here::

                      ┌───────────── minute (0 - 59)
                      │ ┌───────────── hour (0 - 23)
                      │ │ ┌───────────── day of month (1 - 31)
                      │ │ │ ┌───────────── month (1 - 12)
                      │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
                      │ │ │ │ │
                      │ │ │ │ │
    record_interval = * * * * *

Pump triggering strategy
^^^^^^^^^^^^^^^^^^^^^^^^

The watering time is defined in the `Configuration`_. The rational to dissociate the pump stop
from the humidity level measured is the soil slow absorption.

Two modes are available to detect if watering is required by your plants depending on your
configuration.

 - **analog channels available**: the pump is triggered if more than half sensors goes below the
   defined humidity threshold (in %).
 - **else only digital channels**: the pump is triggered if more than half sensors is triggered
   (in this case threshold is generally defined manually directly on the sensor).

Install developing version
--------------------------

If you want to use an unofficial version of the ``pih2o`` application, you need to work from a
clone of this ``git`` repository. Replace the step 5. of the `Install`_ procedure above by the
following actions:

- clone from github ::

   $ git clone https://github.com/anxuae/piH2O.git

- go in the cloned directory ::

   $ cd pih2o

- install ``pih2o`` in editable mode ::

   $ pip3 install -e . --user

- start the application exactly in the same way as installed from pypi. All modifications performed
  in the cloned repository are taken into account when the application starts.

Configuration
-------------

At the first run, a configuration file is generated in ``~/.config/pih2o/pih2o.cfg``
which permits to configure the behavior of the application. The configuration can be
easily edited using the command::

    $ pih2o --config

The default configuration can be restored with the command (strongly recommended when
upgrading ``pih2o``)::

    $ pih2o --reset

See the `default configuration file <https://github.com/anxuae/pih2o/blob/master/docs/config.rst>`_
for further details.

Circuit diagram
---------------

.. image:: https://raw.githubusercontent.com/anxuae/pih2o/master/templates/sketch.png
   :align: center
   :alt: Electronic sketch
