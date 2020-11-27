
import json

from app.models import PowerUnit


def test_add_power_unit(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/power_units',
        data=json.dumps({
            'power_unit': 200345,
            'notes': 'test notes'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert '200345 was added!' in data['message']


def test_add_power_unit_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/power_units',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_power_unit_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/power_units',
        data=json.dumps({"power_units": 200987}), # should be power_unit (no 's')
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_power_unit_duplicate(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/power_units',
        data=json.dumps({
            'power_unit': 200123,
            'notes': 'test notes random'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/power_units',
        data=json.dumps({
            'power_unit': 200123,
            'notes': 'test notes random'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That power unit already exists.' in data['message']


def test_single_power_unit(test_app, test_database, add_power_unit):
    power_unit = add_power_unit(power_unit=300123, notes='just another test note')
    # db.session.add(power_unit)
    # db.session.commit()

    client = test_app.test_client()
    resp = client.get(f'/power_units/{power_unit.id}')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert isinstance(data, dict)
    assert data['power_unit'] == 300123
    assert 'just another test note' in data['notes']


def test_single_power_unit_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/power_units/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'Power unit 999 does not exist' in data['message']


def test_all_power_units(test_app, test_database, add_power_unit):
    test_database.session.query(PowerUnit).delete()
    add_power_unit(700000, 'michael@test.org')
    add_power_unit(800000, 'fletcher@notreal.com')

    client = test_app.test_client()
    resp = client.get('/power_units')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert 700000 == data[0]['power_unit']
    assert 'michael@test.org' in data[0]['notes']
    assert 800000 == data[1]['power_unit']
    assert 'fletcher@notreal.com' in data[1]['notes']


def test_remove_power_unit(test_app, test_database, add_power_unit):
    test_database.session.query(PowerUnit).delete()
    power_unit = add_power_unit(455463, "more notes")

    client = test_app.test_client()
    resp_one = client.get("/power_units")
    data = json.loads(resp_one.data.decode())

    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/power_units/{power_unit.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert '455463 was removed!' in data['message']

    resp_three = client.get("/power_units")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_power_unit_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/power_units/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Power unit 999 does not exist" in data["message"]


def test_update_power_unit(test_app, test_database, add_power_unit):
    power_unit = add_power_unit(200100, "update-me@email.io")
    client = test_app.test_client()

    resp = client.get(f"/power_units/{power_unit.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200

    resp_one = client.put(
        f"/power_units/{power_unit.id}",
        data=json.dumps({"power_unit": 200111, "notes": "new notes"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{power_unit.id} was updated!" in data["message"]

    resp_two = client.get(f"/power_units/{power_unit.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert 200111 == data["power_unit"]
    assert "new notes" in data["notes"]


def test_update_power_unit_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units/1",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_power_unit_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units/1",
        data=json.dumps({"email": "me@email.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_power_unit_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units/999",
        data=json.dumps({"power_unit": 200678, "notes": "test notes"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Power unit 999 does not exist" in data["message"]
