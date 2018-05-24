RESTful API
-----------

This document describe the API exposed by ``pih2o``. The syntax used is close
to the ``curl`` one, but for readability reasons, not all options are written
and the address is truncated (URL without scheme, domain and port).

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

    GET /pih2o/api/v1.0/config

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

    GET /pih2o/api/v1.0/config/<section>'

.. code-block:: json

    {
       "autostart":true
    }


**Get value of an option**::

    GET /pih2o/api/v1.0/config/<section>/<option>'

.. code-block:: json

    true


**Update the configuration (partial update supported)**::

    PUT /pih2o/api/v1.0/config -d '{"<section>": {"<option>": <value>}}'


**Update a section of the configuration (partial update supported)**::

    PUT /pih2o/api/v1.0/config/<section> -d '{"<option1>": <value1>, <option2>": <value2>}'


**Update value of a specific option**::

    PUT /pih2o/api/v1.0/config/<section>/<option> -d '<value>'


``pump``
^^^^^^^^

::

    GET

``measurements``
^^^^^^^^^^^^^^^^

**Get the 10 last measurements (by default only 10 measurements are returned for any request)**::

    GET /pih2o/api/v1.0/measurements'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": "0x3",
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

    GET /pih2o/api/v1.0/measurements?lim=100'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": "0x3",
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

    GET /pih2o/api/v1.0/measurements?sensor=0x3'

.. code-block:: json

    [
        {
            "humidity": 44.0,
            "id": 10600,
            "record_time": "2018-05-24 20:16:00",
            "sensor": "0x3",
            "triggered": true
        },
        {
            "humidity": 67.0,
            "id": 10530,
            "record_time": "2018-04-24 20:16:00",
            "sensor": "0x3",
            "triggered": false
        }
    ]
