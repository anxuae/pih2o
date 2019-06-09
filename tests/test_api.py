# -*- coding: utf-8 -*-

import json
import pih2o


def test_server_is_up(client):
    resp = client.get('/pih2o')
    assert resp.status_code == 200
    assert json.loads(resp.data) == {"name": pih2o.__name__,
                                     "version": pih2o.__version__,
                                     "running": True}


def test_get_config(client):
    resp = client.get('/pih2o/api/v1/config')
    assert resp.status_code == 200
    assert json.loads(resp.data)["GENERAL"]["autostart"] == False


def test_set_config(client, headers):
    resp = client.put('/pih2o/api/v1/config', headers=headers,
                      data='{"GENERAL":{"autostart":true}}')
    assert resp.status_code == 204

    resp = client.get('/pih2o/api/v1/config')
    assert json.loads(resp.data)["GENERAL"]["autostart"] == True


def test_get_config_section(client):
    resp = client.get('/pih2o/api/v1/config/GENERAL')
    assert resp.status_code == 200
    assert json.loads(resp.data)["autostart"] == False


def test_set_config_section(client, headers):
    resp = client.put('/pih2o/api/v1/config/GENERAL', headers=headers,
                      data='{"autostart":true}')
    assert resp.status_code == 204

    resp = client.get('/pih2o/api/v1/config/GENERAL')
    assert json.loads(resp.data)["autostart"] == True


def test_get_config_value(client):
    resp = client.get('/pih2o/api/v1/config/GENERAL/autostart')
    assert resp.status_code == 200
    assert json.loads(resp.data) == False


def test_set_config_value(client, headers):
    resp = client.put('/pih2o/api/v1/config/GENERAL/autostart', headers=headers,
                      data='true')
    assert resp.status_code == 204

    resp = client.get('/pih2o/api/v1/config/GENERAL/autostart')
    assert json.loads(resp.data) == True


def test_start_pump(client):
    resp = client.get('/pih2o/api/v1/pump')
    assert resp.status_code == 204


def test_start_pump_with_duration(client):
    resp = client.get('/pih2o/api/v1/pump/10')
    assert resp.status_code == 204


def test_get_sensors_list(client):
    resp = client.get('/pih2o/api/v1/sensors')
    assert resp.status_code == 200
    assert json.loads(resp.data) == [0, 1, 2]


def test_read_one_sensor(client):
    resp = client.get('/pih2o/api/v1/sensors/2')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['sensor'] == 2


def test_get_10_measurements(client, db_data):
    resp = client.get('/pih2o/api/v1/measurements')
    assert resp.status_code == 200
    assert list(reversed(db_data))[:10] == json.loads(resp.data)


def test_get_20_measurements(client, db_data):
    resp = client.get('/pih2o/api/v1/measurements?lim=20')
    assert resp.status_code == 200
    assert list(reversed(db_data))[:20] == json.loads(resp.data)


def test_get_sensor(client, db_data):
    resp = client.get('/pih2o/api/v1/measurements?sensor=3')
    assert resp.status_code == 200
    assert len(json.loads(resp.data)) == 5
