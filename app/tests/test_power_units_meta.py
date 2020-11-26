
import json

# from app import db
from app.models import PowerUnit, PowerUnitMeta


def test_add_power_unit_meta(test_app, test_database):
    test_database.session.query(PowerUnit).delete()
    test_database.session.query(PowerUnitMeta).delete()
    client = test_app.test_client()
    # _ = client.post(
    #     '/power_units',
    #     data=json.dumps({
    #         'power_unit': 200345,
    #         'notes': 'test notes'
    #     }),
    #     content_type='application/json',
    # )
    test = test_database.session.query(PowerUnit).all()
    assert len(test) == 0
    
    resp = client.post(
        '/power_units_meta',
        data=json.dumps({
            'id_foreign': 1,
            'element': 'text fill',
            'power_unit': '#717174',
            'notes': '#717174'
        }),
        content_type='application/json',
    )
    test2 = test_database.session.query(PowerUnitMeta).all()
    assert len(test2) == 1
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert '1 was added!' in data['message']


def test_add_power_unit_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/power_units_meta',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_power_unit_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/power_units_meta',
        data=json.dumps({"power_units": 200987}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_power_unit_duplicate(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/power_units_meta',
        data=json.dumps({
            'id_foreign': 1,
            'element': 'text fill',
            'power_unit': '#717174',
            'notes': '#717174'
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/power_units_meta',
        data=json.dumps({
            'id_foreign': 1,
            'element': 'text fill',
            'power_unit': '#717174',
            'notes': '#717174'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That power unit meta already exists.' in data['message']


def test_single_power_unit(test_app, test_database, add_power_units_meta):
    record = add_power_units_meta(
        id_foreign=1,
        element='text fill',
        power_unit='#717174', 
        notes='#919191'
    )
    # db.session.add(power_unit)
    # db.session.commit()

    client = test_app.test_client()
    resp = client.get(f'/power_units_meta/{record.id}')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert isinstance(data, dict)
    assert data['id_foreign'] == 1
    assert data['element'] == 'text fill'
    assert data['power_unit'] == '#717174'
    assert data['notes'] == '#919191'


def test_single_power_unit_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/power_units_meta/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'ID foreign 999 does not exist' in data['message']


def test_all_power_units(test_app, test_database, add_power_units_meta):
    test_database.session.query(PowerUnitMeta).delete()
    add_power_units_meta(
        id_foreign=1,
        element='text fill',
        power_unit='#717174', 
        notes='#919100'
    )
    add_power_units_meta(
        id_foreign=2,
        element='cell fill',
        power_unit='#717199', 
        notes='#919191'
    )

    client = test_app.test_client()
    resp = client.get('/power_units_meta')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert len(data) == 2
    assert data[0]['power_unit'] == '#717174'
    assert data[1]['power_unit'] == '#717199'
    assert data[0]['notes'] == '#919100'
    assert data[1]['notes'] == '#919191'


def test_remove_power_unit(test_app, test_database, add_power_units_meta):
    test_database.session.query(PowerUnitMeta).delete()
    record = add_power_units_meta(
        id_foreign=2,
        element='cell fill',
        power_unit='#717199', 
        notes='#919191'
    )

    client = test_app.test_client()
    resp_one = client.get("/power_units_meta")
    data = json.loads(resp_one.data.decode())

    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/power_units_meta/{record.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert '2 was removed!' in data['message']

    resp_three = client.get("/power_units")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_power_unit_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/power_units_meta/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "ID foreign 999 does not exist" in data["message"]


def test_update_power_unit(test_app, test_database, add_power_units_meta):
    record = add_power_units_meta(
        id_foreign=2,
        element='cell fill',
        power_unit='#717199', 
        notes='#919191'
    )
    client = test_app.test_client()

    resp = client.get(f"/power_units_meta/{record.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200

    resp_one = client.put(
        f"/power_units_meta/{record.id}",
        data=json.dumps({
            'id_foreign': 1,
            'element': 'text fill',
            'power_unit': '#717100',
            'notes': '#919100',
        }),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{record.id} was updated!" in data["message"]

    resp_two = client.get(f"/power_units_meta/{record.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert data["id_foreign"] == 1
    assert data["element"] == 'text fill'
    assert data["power_unit"] == '#717100'
    assert data["notes"] == '#919100'


def test_update_power_unit_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units_meta/1",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_power_unit_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units_meta/1",
        data=json.dumps({"email": "me@email.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_power_unit_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/power_units_meta/999",
        data=json.dumps({
            'id_foreign': 1,
            'element': 'text fill',
            'power_unit': '#717100',
            'notes': '#919100',
        }),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "ID foreign 999 does not exist" in data["message"]
