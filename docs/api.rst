RESTful API
-----------

This document describe the API exposed by ``pih2o``. The syntax used is close
to the ``curl`` one, but for readability reasons, not all options are written
and the address is truncated (URL without scheme, domain and port).

.. contents:: API Contents:


``pih2o``
^^^^^^^^^

**Server information**::

    GET /pih2o

.. code-block:: json

    {
       "name":"pih2o",
       "version":"0.0.0"
    }


``config``
^^^^^^^^^^


**Get entire configuration**::

    GET /pih2o/api/v1/config

.. code-block:: json

    {
       "GENERAL":{
          "autostart":true
       },
       "PUMP":{
          "pin":3,
          "flow":500
       }
    }


**Get all options from a section**::

    GET /pih2o/api/v1/config/<section>'

.. code-block:: json

    {
       "autostart":true
    }


**Get value of an option**::

    GET /pih2o/api/v1/config/<section>/<option>'

.. code-block:: json

    true


**Update the configuration (partial update supported)**::

    PUT /pih2o/api/v1/config -d '{"<section>": {"<option>": <value>}}'


**Update a section of the configuration (partial update supported)**::

    PUT /pih2o/api/v1/config/<section> -d '{"<option1>": <value1>, <option2>": <value2>}'


**Update value of a specific option**::

    PUT /pih2o/api/v1/config/<section>/<option> -d '<value>'


``pump``
^^^^^^^^


**Start wateing pump for duration defined in the configuration**::

    GET /pih2o/api/v1/pump'


**Start wateing pump for 10 seconds**::

    GET /pih2o/api/v1/pump/10'


``sensors``
^^^^^^^^^^^


**Get the sensors list IDs (corresponds to the connection pin)**::

    GET /pih2o/api/v1/sensors'

.. code-block:: json

    [
        1,
        2,
        3,
        4
    ]


**Get value of the sensor with ID 3**::

    GET /pih2o/api/v1/sensors/3'

.. code-block:: json

    {
        "humidity": 33,
        "id": null,
        "record_time": "2018-05-26 10:02:41",
        "sensor": 3,
        "triggered": false
    }


``measurements``
^^^^^^^^^^^^^^^^

**Get the 10 last measurements (by default only 10 measurements are returned for any request)**::

    GET /pih2o/api/v1/measurements'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": 3,
            "triggered": false
        },

        ...

        {
            "humidity": 26.0,
            "id": 10591,
            ...
        }
    ]

**Get the 100 last measurements**::

    GET /pih2o/api/v1/measurements?lim=100'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": 3,
            "triggered": false
        },

        ...

        {
            "humidity": 26.0,
            "id": 10591,
            ...
        }
    ]

**Get measurements from a specific sensor**::

    GET /pih2o/api/v1/measurements?sensor=3'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": 3,
            "triggered": true
        },
        {
            "humidity": 67.0,
            "id": 10530,
            "record_time": "2018-04-24 20:16:00",
            "sensor": 3,
            "triggered": false
        }
    ]

**Get measurements using several query string filters**::

    GET /pih2o/api/v1/measurements?sensor=3&humidity=44.0'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": 3,
            "triggered": true
        }
    ]
