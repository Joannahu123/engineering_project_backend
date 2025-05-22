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
    @staticmethod
    def get_posting(name):
        posting = {
            "martha": {
                "name": "martha",
                "dish": "cornbread",
                "cuisine": "american",
                "link": "https://www.marthastewart.com/859136/classic-cornbread",
                "comments": "tastes amazing, very quick and easy to make to. Highly recommend for those who want to make cornbread",


            },
            "wayne": {
                "name": "wayne",
                "dish": "stir fry tofu",
                "cuisine": "chinese",
                "link": "https://rainbowplantlife.com/tofu-stir-fry/",
                "comments": "very savory flavors and pretty simple ingredients everybody has at home. Would recommend",
            },
        }
        return posting.get(name)


    class _wayne(Resource):
        def get(self):
            posting = postingAPI.get_posting("wayne")
            if posting:
                return jsonify(posting)
            return {"Data not found"}, 404
    class _martha(Resource):
        def get(self):
            posting = postingAPI.get_posting("martha")
            if posting:
                return jsonify(posting)
            return {"Data not found"}, 404
    class _createPosting(Resource):
            def post(self):
                """
                sCreate new posting.
                """
                body = request.get_json()
                name = body.get('name')
                dish = body.get('dish')
                cuisine = body.get('cuisine')
                link = body.get('link')
                comments = body.get('comments')


                # Validate name
                name = body.get('name')
                if name is None or len(name) < 2:
                    return {'message': 'Name is missing, or is less than 2 characters'}, 400


                dish = body.get('dish')
                if dish is None:
                    return {'message': 'dish is missing'}, 400
               
                cuisine = body.get('cuisine')
                if cuisine is None:
                    return {'message': 'cuisine is missing'}, 400
               
                link = body.get('link')
                if link is None or len(link) < 2:
                    return {'message': 'link is missing, or is less than 2 characters'}, 400
               
                comments = body.get('comments')
                if comments is None:
                    return {'message': 'comments are missing, or is less than 2 characters'}, 400
               
                # Setup minimal posting OBJECT
                posting_obj = Posting(name=name, dish=dish, cuisine=cuisine, link=link, comments=comments)
                posting = posting_obj.create()

                # Add user to database
                posting = posting_obj.create()  # pass the body elements to be saved in the database
                if not posting:  # failure returns error message
                    return {'message': f'Processed {name}'}, 400
                return jsonify(posting.read())
    class _Read(Resource):
        def get(self, name=None):
            """
            Retrieve posts. If name is provided, fetch that post; otherwise, return all posts.
            """
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
            """SSS
            Retrieve a single Post by their name.
            """
            try:
                posting = Posting.query.all()

                posting_data = [posting.read() for posting in posting]

                return jsonify(posting_data)
            except Exception as e:
                return {'message': f'Error retrieving post: {str(e)}'}, 500
    
    
    class _Update(Resource):
        def put(self):
            """
            Update
            """
            body = request.get_json()

            name = body.get('name')
            if not name:
                return {'message': 'Name is required for updating.'}, 400


            posting = Posting.query.filter_by(name=name).first()
            if posting is None:
                return {'message': f'Posting {name} not found'}, 404

            updated_fields = []
            if 'dish' in body:
                posting.dish = body['dish']
                updated_fields.append('dish')
            if 'cuisine' in body:
                posting.cuisine = body['cuisine']
                updated_fields.append('cuisine')
            if 'link' in body:
                posting.link = body['link']
                updated_fields.append('link')
            if 'comments' in body:
                posting.comments = body['comments']
                updated_fields.append('comments')

            posting.update(body)
            return jsonify(posting.read())
        

    class _Delete(Resource):
        def delete(self):
            """
            Delete a post by name.
            """
            body = request.get_json()
            name = body.get('name')

         # Check if 'name' is provided in the request body
            if not name:
                return {'message': 'Missing posting name'}, 400  # Bad request

            # Find the posting by name
            posting = Posting.query.filter_by(name=name).first()

            if posting is None:
                return {'message': f'Posting {name} not found'}, 404  # Not found

            # Serialize data before deletion
            deleted_data = posting.read()
            #actually delete the post
            db.session.delete(posting)  # Remove post from database
            db.session.commit()

            # Proceed to delete the post
            return ({'message': f'Posting {name} deleted', 'data': deleted_data}), 200



    
    class _getPosting(Resource):
        def get(self, name):
            posting = Posting.query.filter(Posting.name.ilike(name)).first()  # Case insensitive search
            if posting:
                return posting.read(), 200 # Return dictionary in JSON format
            return {"message": "Data not found"}, 404
       






    # building RESTapi endpoint
api.add_resource(postingAPI._martha, '/posting/martha')          
api.add_resource(postingAPI._wayne, '/posting/wayne')
api.add_resource(postingAPI._createPosting, '/posting/create')
api.add_resource(postingAPI()._getPosting, '/posting/read/<string:name>')
api.add_resource(postingAPI._Read, '/posting/reading')
api.add_resource(postingAPI._ReadGeneral, '/posting/Get/')
api.add_resource(postingAPI._Update, '/posting/update/')
api.add_resource(postingAPI._Delete, '/posting/delete')




# Instantiate the posting_api to register the endpoints
posting_api_instance = postingAPI()

if __name__ == '__main__':
    app.run(port=8887)

   
