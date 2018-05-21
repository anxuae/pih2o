# -*- coding: utf-8 -*-

import pytest
import pih2o


@pytest.fixture
def client(tmpdir):
    cfgfile = str(tmpdir.mkdir(".config").join("pih2o.cfg"))
    app = pih2o.create_app(cfgfile)
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@pytest.fixture
def headers():
    return {'content-type': 'application/json'}
