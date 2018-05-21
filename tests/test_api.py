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
    resp = client.get('/pih2o/api/v1.0/config')
    assert resp.status_code == 200
    assert json.loads(resp.data)["GENERAL"]["autostart"] is True


def test_set_config(client, headers):
    resp = client.put('/pih2o/api/v1.0/config', headers=headers,
                      data='{"GENERAL":{"autostart":false}}')
    assert resp.status_code == 204


def test_get_config_section(client):
    resp = client.get('/pih2o/api/v1.0/config/GENERAL')
    assert resp.status_code == 200
    assert json.loads(resp.data)["autostart"] is True


def test_set_config_section(client, headers):
    resp = client.put('/pih2o/api/v1.0/config/GENERAL', headers=headers,
                      data='{"autostart":false}')
    assert resp.status_code == 204


def test_get_config_value(client):
    resp = client.get('/pih2o/api/v1.0/config/GENERAL/autostart')
    assert resp.status_code == 200
    assert json.loads(resp.data) is True


def test_set_config_value(client, headers):
    resp = client.put('/pih2o/api/v1.0/config/GENERAL/autostart', headers=headers,
                      data='false')
    assert resp.status_code == 204
