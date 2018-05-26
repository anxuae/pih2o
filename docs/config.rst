
Default configuration
---------------------

.. code-block:: ini

    [GENERAL]
    # Start pih2o at Raspberry Pi startup
    autostart = True

    # Time between each humidity measurement
    record_interval = 0 19 * * *

    # Percentage under which a sensor is considered as triggered
    humidity_threshold = 20

    [PUMP]
    # Physical GPIO pin where the pump is connected (or electro-valve)
    pin = 7

    # Watering duration in seconds when the pump is started
    duration = 60

    [SENSOR]
    # Physical GPIO DO-OUT pin use to power on/off the sensors
    power_pin = 12

    # True if need to power on the sensors continuously (accelerate corrosion of resistive sensors)
    always_powered = False

    # Physical GPIO DO-IN pins to detect threshold exceeded
    digital_pins = (11, 15, 31)

    # ADS1115 channels used to read the humidity level
    analog_pins = (1, 2, 3)

    # Sensor physical range measured with the ADS1115 (from dry to wet)
    analog_range = (0, 970)
