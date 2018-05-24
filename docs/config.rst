
Default configuration
---------------------

.. code-block:: ini

    [GENERAL]
    # Start pih2o at Raspberry Pi startup
    autostart = True

    # Time between each humidity measurement
    record_interval = 0 19 * * *

    [PUMP]
    # Physical GPIO pin where the pump is connected (or electro-valve)
    pin = 7

    # Watering duration in seconds when the pump is started
    duration = 60

    [SENSORS]
    # ADS1115 channels used to read the humidity level (4 max)
    analog_pins = (1, 2, 3, 4)

    # Physical GPIO pins to detect threshold exceeded (4 max)
    digital_pins = (11, 13, 15, 16)

    # Percentage under which a sensor is considered as triggered
    analog_threshold = 20
