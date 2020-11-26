
from flask import request
from flask_restx import Resource, fields, Namespace
# from flask_restplus_sqlalchemy import ApiModelFactory

from app import db
from app.models import PowerUnitMeta


power_units_meta_namespace = Namespace('power_units_meta')


power_units_meta_model = power_units_meta_namespace.model(
    'PowerUnitMeta', {
        'id': fields.Integer(readonly=True),
        'id_foreign': fields.Integer(required=True),
        'element': fields.String(required=True),
        'power_unit': fields.String(required=True),
        'notes': fields.String(),
    }
)

# Link Flask Rest Plus API with SQLAlchemy
# api_model_factory = ApiModelFactory(api=power_units_meta_namespace, db=db)
# power_units_meta_model = api_model_factory.get_entity(PowerUnitMeta.__tablename__)


class PowerUnitsMetaList(Resource):

    @power_units_meta_namespace.expect(power_units_meta_model, validate=True)
    def post(self):
        post_data = request.get_json()
        cols = {}
        cols['id_foreign'] = post_data.get('id_foreign')
        cols['element'] = post_data.get('element')
        cols['power_unit'] = post_data.get('power_unit')
        cols['notes'] = post_data.get('notes')
        response_object = {}

        record = PowerUnitMeta.query.filter_by(id_foreign=cols['id_foreign']).first()
        if record:
            response_object['message'] = 'Sorry. That power unit meta already exists.'
            return response_object, 400

        record = PowerUnitMeta()
        for key, value in cols.items():
            setattr(record, key, value)

        db.session.add(record)
        db.session.commit()

        response_object['message'] = f"{cols['id_foreign']} was added!"
        return response_object, 201

    @power_units_meta_namespace.marshal_with(power_units_meta_model, as_list=True)
    def get(self):
        return PowerUnitMeta.query.all(), 200


class PowerUnitsMeta(Resource):

    @power_units_meta_namespace.marshal_with(power_units_meta_model)
    def get(self, id_):
        record = PowerUnitMeta.query.filter_by(id=id_).first()
        if record is None:
            power_units_meta_namespace.abort(404, f"ID foreign {id_} does not exist")
        
        return record, 200

    def delete(self, id_):
        response_object = {}
        record = PowerUnitMeta.query.filter_by(id=id_).first()

        if not record:
            power_units_meta_namespace.abort(404, f"ID foreign {id_} does not exist")

        db.session.delete(record)
        db.session.commit()

        response_object["message"] = f"{record.id_foreign} was removed!"
        return response_object, 200

    @power_units_meta_namespace.expect(power_units_meta_model, validate=True)
    def put(self, id_):
        post_data = request.get_json()
        cols = {}
        cols['id_foreign'] = post_data.get('id_foreign')
        cols['element'] = post_data.get('element')
        cols['power_unit'] = post_data.get('power_unit')
        cols['notes'] = post_data.get('notes')
        response_object = {}

        record = PowerUnitMeta.query.filter_by(id=id_).first()
        if not record:
            power_units_meta_namespace.abort(404, f"ID foreign {id_} does not exist")

        for key, value in cols.items():
            setattr(record, key, value)

        db.session.commit()

        response_object["message"] = f"{record.id} was updated!"
        return response_object, 200


power_units_meta_namespace.add_resource(PowerUnitsMetaList, '')
power_units_meta_namespace.add_resource(PowerUnitsMeta, '/<int:id_>')
