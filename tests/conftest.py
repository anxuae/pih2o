# -*- coding: utf-8 -*-

import random
import datetime
import pytest
import pih2o
from pih2o import models


@pytest.fixture()
def client(tmpdir):
    cfgfile = str(tmpdir.mkdir(".config").join("pih2o.cfg"))
    app = pih2o.create_app(cfgfile)
    app.config['TESTING'] = True
    client = app.test_client()
    client.app = app

    yield client


@pytest.fixture()
def db_data(client):
    data = []
    count = 1
    with client.app.app_context():
        for i in range(5):
            for j in range(4):
                humidity = float(random.randint(2, 99))
                date = datetime.datetime.now() + datetime.timedelta(seconds=i * 300)
                measurement = models.Measurement(sensor=j,
                                                 humidity=humidity,
                                                 triggered=humidity < 30,
                                                 record_time=date)
                models.db.session.add(measurement)
                d = measurement.json()
                d[u'id'] = count
                data.append(d)
                count += 1
        models.db.session.commit()
    return data


@pytest.fixture
def headers():
    return {'content-type': 'application/json'}
