from flask import Blueprint, jsonify, request, g
import logging
from flask_restful import Api, Resource
from model.posting import Posting # used for REST API building
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database-file.db'  # Update with your database URI
from model.posting import db

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)



posting_api = Blueprint('posting_api', __name__, url_prefix='/api')


# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(posting_api)



class postingAPI:

    class _createPosting(Resource):
        def post(self):
            body = request.get_json()
            name = body.get('name')
            school = body.get('school')
            engineeringType = body.get('engineeringType')
            partUsed = body.get('partUsed')
            description = body.get('description')

            # Validate required fields
            if name is None or len(name) < 2:
                return {'message': 'Name is missing or too short'}, 400
            if school is None:
                return {'message': 'School is missing'}, 400
            if engineeringType is None:
                return {'message': 'Engineering type is missing'}, 400
            if partUsed is None:
                return {'message': 'Part used is missing'}, 400
            if description is None:
                return {'message': 'Description is missing'}, 400

            # Create and save posting
            posting_obj = Posting(
                name=name,
                school=school,
                engineeringType=engineeringType,
                partUsed=partUsed,
                description=description
            )
            posting = posting_obj.create()

            if not posting:
                return {'message': f'Failed to create post for {name}'}, 400
            return jsonify(posting.read())


    class _Read(Resource):
        def get(self, name=None):
            try:
                if name:
                    posting = Posting.query.filter_by(name=name).first()
                    return jsonify(posting.read()) if posting else {'message': f'Post "{name}" not found'}, 404
                else:
                    postings = Posting.query.all()
                    return jsonify([post.read() for post in postings])
            except Exception as e:
                return {'message': f'Error retrieving post: {str(e)}'}, 500


    class _ReadGeneral(Resource):
        def get(self):
            try:
                postings = Posting.query.all()
                return jsonify([post.read() for post in postings])
            except Exception as e:
                return {'message': f'Error retrieving posts: {str(e)}'}, 500


    class _Update(Resource):
        def put(self):
            body = request.get_json()
            name = body.get('name')
            if not name:
                return {'message': 'Name is required for updating.'}, 400

            posting = Posting.query.filter_by(name=name).first()
            if posting is None:
                return {'message': f'Posting {name} not found'}, 404

            posting.update(body)
            return jsonify(posting.read())


    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            name = body.get('name')
            if not name:
                return {'message': 'Missing posting name'}, 400

            posting = Posting.query.filter_by(name=name).first()
            if posting is None:
                return {'message': f'Posting {name} not found'}, 404

            deleted_data = posting.read()
            db.session.delete(posting)
            db.session.commit()
            return {'message': f'Posting {name} deleted', 'data': deleted_data}, 200


    class _getPosting(Resource):
        def get(self, name):
            posting = Posting.query.filter(Posting.name.ilike(name)).first()
            if posting:
                return posting.read(), 200
            return {"message": "Data not found"}, 404


# Registering API endpoints
api.add_resource(postingAPI._createPosting, '/posting/create')
api.add_resource(postingAPI._getPosting, '/posting/read/<string:name>')
api.add_resource(postingAPI._Read, '/posting/reading')
api.add_resource(postingAPI._ReadGeneral, '/posting/Get/')
api.add_resource(postingAPI._Update, '/posting/update/')
api.add_resource(postingAPI._Delete, '/posting/delete')
