RESTful API
-----------

This document describe the API exposed by ``pih2o``. The syntax used is close
to the ``curl`` one, but for readability reasons, not all options are written
and the address is truncated (URL without scheme, domain and port).

``server``
^^^^^^^^^^

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

``data``
^^^^^^^^

::

    GET
