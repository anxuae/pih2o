
Default configuration
---------------------

.. code-block:: ini

    [GENERAL]
    # Start pih2o at Raspberry Pi startup (useful if pih2o not running with a WSGI)
    autostart = False

    # Time between each humidity measurement
    record_interval = 0 19 * * *

    # Percentage under which a sensor is considered as triggered
    humidity_threshold = 20

    # Rules applied to trigger the pump ('first', 'majority' or 'last')
    watering_strategy = majority

    [PUMP]
    # Physical GPIO pin where the pump is connected (or electro-valve)
    pin = 7

    # Watering duration in seconds when the pump is started
    duration = 60

    [SENSOR]
    # Physical GPIO DO-OUT pin use to power on/off the sensors
    power_pin = 12

    # Physical GPIO DO-IN pins to detect threshold exceeded
    digital_pins = (11, 13, 15)

    # ADS1115 channels used to read the humidity level
    analog_pins = (0, 1, 2)

    # Sensor physical range measured with the ADS1115 (from wet to dry)
    analog_range = (15900, 32800)
