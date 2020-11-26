# from app.api import bp

# @bp.route('/power_units_meta/<int:id>', methods=['GET'])
# def get_power_unit_meta(id):
#     pass

# @bp.route('/power_units_meta', methods=['GET'])
# def get_power_unit_metas_meta():
#     pass

# @bp.route('/power_units_meta', methods=['POST'])
# def create_power_unit_meta():
#     pass

# @bp.route('/power_units_meta/<int:id>', methods=['PUT'])
# def update_power_unit_meta(id):
#     pass



from flask import request
from flask_restx import Resource, fields, Namespace
# from flask_restplus_sqlalchemy import ApiModelFactory

from app import db
from app.models import PowerUnit


power_units_namespace = Namespace('power_units')


power_units_model = power_units_namespace.model(
    'PowerUnit', {
        'id': fields.Integer(readonly=True),
        'power_unit': fields.Integer(required=True),
        'notes': fields.String(),
    }
)

# Link Flask Rest Plus API with SQLAlchemy
# api_model_factory = ApiModelFactory(api=power_units_namespace, db=db)
# power_units_model = api_model_factory.get_entity(PowerUnit.__tablename__)


class PowerUnitsList(Resource):

    @power_units_namespace.expect(power_units_model, validate=True)
    def post(self):
        post_data = request.get_json()
        power_unit = post_data.get('power_unit')
        notes = post_data.get('notes')
        response_object = {}

        pu = PowerUnit.query.filter_by(power_unit=power_unit).first()
        if pu:
            response_object['message'] = 'Sorry. That power unit already exists.'
            return response_object, 400

        db.session.add(PowerUnit(power_unit=power_unit, notes=notes))
        db.session.commit()

        response_object['message'] = f'{power_unit} was added!'
        return response_object, 201

    @power_units_namespace.marshal_with(power_units_model, as_list=True)
    def get(self):
        return PowerUnit.query.all(), 200


class PowerUnits(Resource):

    @power_units_namespace.marshal_with(power_units_model)
    def get(self, power_unit_id):
        pu = PowerUnit.query.filter_by(id=power_unit_id).first()
        if pu is None:
            power_units_namespace.abort(404, f"Power unit {power_unit_id} does not exist")
        
        return pu, 200

    def delete(self, power_unit_id):
        response_object = {}
        pu = PowerUnit.query.filter_by(id=power_unit_id).first()

        if not pu:
            power_units_namespace.abort(404, f"Power unit {power_unit_id} does not exist")

        db.session.delete(pu)
        db.session.commit()

        response_object["message"] = f"{pu.power_unit} was removed!"
        return response_object, 200

    @power_units_namespace.expect(power_units_model, validate=True)
    def put(self, power_unit_id):
        post_data = request.get_json()
        power_unit = post_data.get("power_unit")
        notes = post_data.get("notes")
        response_object = {}

        pu = PowerUnit.query.filter_by(id=power_unit_id).first()
        if not pu:
            power_units_namespace.abort(404, f"Power unit {power_unit_id} does not exist")

        pu.power_unit = power_unit
        pu.notes = notes
        db.session.commit()

        response_object["message"] = f"{pu.power_unit} was updated!"
        return response_object, 200


power_units_namespace.add_resource(PowerUnitsList, '')
power_units_namespace.add_resource(PowerUnits, '/<int:power_unit_id>')
