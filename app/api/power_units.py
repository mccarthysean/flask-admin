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



from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app import db
from app.models import PowerUnit


power_units_blueprint = Blueprint('power_units', __name__)
api = Api(power_units_blueprint)

power_unit_model = api.model('PowerUnit', {
    'id': fields.Integer(readonly=True),
    'power_unit': fields.Integer(required=True),
    'notes': fields.String(),
})

class PowerUnitsList(Resource):

    @api.expect(power_unit_model, validate=True)
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

    @api.marshal_with(power_unit_model, as_list=True)
    def get(self):
        return PowerUnit.query.all(), 200


class PowerUnits(Resource):

    @api.marshal_with(power_unit_model)
    def get(self, power_unit_id):
        pu = PowerUnit.query.filter_by(id=power_unit_id).first()
        if pu is None:
            api.abort(404, f"Power unit {power_unit_id} does not exist")
        
        return pu, 200

    def delete(self, power_unit_id):
        response_object = {}
        pu = PowerUnit.query.filter_by(id=power_unit_id).first()

        if not pu:
            api.abort(404, f"Power unit {power_unit_id} does not exist")

        db.session.delete(pu)
        db.session.commit()

        response_object["message"] = f"{pu.power_unit} was removed!"
        return response_object, 200

    @api.expect(power_unit_model, validate=True)
    def put(self, power_unit_id):
        post_data = request.get_json()
        power_unit = post_data.get("power_unit")
        notes = post_data.get("notes")
        response_object = {}

        pu = PowerUnit.query.filter_by(id=power_unit_id).first()
        if not pu:
            api.abort(404, f"Power unit {power_unit_id} does not exist")

        pu.power_unit = power_unit
        pu.notes = notes
        db.session.commit()

        response_object["message"] = f"{pu.power_unit} was updated!"
        return response_object, 200


api.add_resource(PowerUnitsList, '/power_units')
api.add_resource(PowerUnits, '/power_units/<int:power_unit_id>')
