
from flask import request
from flask_restx import Resource, fields, Namespace
# from flask_restplus_sqlalchemy import ApiModelFactory

from app import db
from app.models import MetaData


meta_data_namespace = Namespace('meta_data')

meta_data_model = meta_data_namespace.model(
    'MetaData', {
        'id': fields.Integer(readonly=True),
        'id_cell': fields.String(required=True),
        'element': fields.String(required=True),
        'color': fields.String(required=True),
    }
)

# Link Flask Rest Plus API with SQLAlchemy
# api_model_factory = ApiModelFactory(api=meta_data_namespace, db=db)
# meta_data_model = api_model_factory.get_entity(MetaData.__tablename__)


class MetaDataList(Resource):

    @meta_data_namespace.marshal_with(meta_data_model, as_list=True)
    def get(self):
        """Returns a list of all records"""
        return MetaData.query.all(), 200

    @meta_data_namespace.expect(meta_data_model, validate=True)
    def post(self):
        """Creates a single record. If record exists, it updates it."""
        post_data = request.get_json()
        id_cell = post_data.get('id_cell')
        element = post_data.get('element')
        color = post_data.get('color')
        response_object = {}

        record = MetaData.query.filter_by(id_cell=id_cell, element=element).first()
        if record is None:
            # Create a new record
            record = MetaData(id_cell=id_cell, element=element, color=color)
            db.session.add(record)
            response_object['message'] = 'Record was created!'
        else:
            # Update existing record, like a put request
            # response_object['message'] = 'That record already exists.'
            # return response_object, 400
            record.color = color
            response_object['message'] = 'Record was updated!'

        db.session.commit()

        return response_object, 201


class MetaDataIndividual(Resource):

    @meta_data_namespace.marshal_with(meta_data_model)
    def get(self, id_cell):
        """Returns a single record"""
        record = MetaData.query.filter_by(id_cell=id_cell).first()
        if record is None:
            meta_data_namespace.abort(404, "That record does not exist")
        
        return record, 200

    def delete(self, id_cell):
        """Deletes a single record"""
        response_object = {}
        record = MetaData.query.filter_by(id_cell=id_cell).first()

        if not record:
            meta_data_namespace.abort(404, "That record does not exist")

        db.session.delete(record)
        db.session.commit()

        response_object["message"] = f"{record.id_cell} was removed!"
        return response_object, 200

    @meta_data_namespace.expect(meta_data_model, validate=True)
    def put(self, id_cell):
        """Updates a single record"""

        post_data = request.get_json()
        # The new id_cell, if it needs to be changed
        # new_id_cell = post_data.get("id_cell")
        element = post_data.get("element")
        color = post_data.get("color")
        response_object = {}

        record = MetaData.query.filter_by(id_cell=id_cell).first()
        if not record:
            response_object['message'] = 'That record does not exist.'
            return response_object, 400

        # record.id_cell = new_id_cell
        record.element = element
        record.color = color
        db.session.commit()

        # response_object["message"] = f"id_cell '{id_cell}' was updated to id_cell '{new_id_cell}', element '{element}', and color '{color}'"
        response_object["message"] = "Successfully updated"
        return response_object, 200


meta_data_namespace.add_resource(MetaDataList, '')
meta_data_namespace.add_resource(MetaDataIndividual, '/<string:id_cell>')
