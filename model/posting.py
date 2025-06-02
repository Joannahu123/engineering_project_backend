from sqlite3 import IntegrityError
from __init__ import app, db


class Posting(db.Model):
    __tablename__ = 'posting'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    school = db.Column(db.String(100))            # add
    engineeringType = db.Column(db.String(100))   # add
    partUsed = db.Column(db.String(255))          # add
    description = db.Column(db.Text)               # add


    def __init__(self, name, school, engineeringType, partUsed, description):
        self.name = name
        self.school = school
        self.engineeringType = engineeringType
        self.partUsed = partUsed
        self.description = description


    def create(self):
        try:
            db.session.add(self)  # Prepare to persist posting object to the postings table
            db.session.commit()  # Commit the changes to the database
            return self
        except IntegrityError:
            db.session.rollback()
            return None



    def read(self):
        return {
            "name": self.name,
            "school": self.school,
            "engineeringType": self.engineeringType,
            "partUsed": self.partUsed,
            "description": self.description,
        }


    def update(self, inputs):
            """
            Updates the student object with new data.
           
            Args:
                inputs (dict): A dictionary containing the new data for the student.
           
            Returns:
                Student: The updated user object, or None on error.
            """
            if not isinstance(inputs, dict):
                return self


            name = inputs.get("name", "")
            school = inputs.get("school", "")
            engineeringType = inputs.get("engineeringType", "")
            partUsed = inputs.get("partUsed", "")
            description = inputs.get("description", "")


            # Update table with new data
            if name:
                self.name = name
            if school:
                self.school = school
            if engineeringType:
                self.engineeringType = engineeringType
            if partUsed:
                self.partUsed = partUsed
            if description:
                self.description = description
               
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return None
            return self
    def delete(self):
        """
        Removes the user object from the database and commits the transaction.
       
        Returns:
            None
        """
            # try:
            # # posting_to_delete = Posting.query.filter_by(name=self.name).first()
            # # if posting_to_delete:
            #     db.session.delete(posting_to_delete)
            #     db.session.commit()
            # # else:
            # #     return None
            # # except IntegrityError:
            # # db.session.rollback()
            # # return None
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return None  




    def restore(data):
            posting = {}
            for posting_data in data:
                _ = posting_data.pop('id', None)  # Remove 'id' from user_data and store it in user_id
                _name = posting_data.get("name", None)
                posting = Posting.query.filter_by(name=_name).first()
                print(type(posting))
                if posting:
                    posting.update(posting_data)
                else:
                    posting = Posting(**posting_data)
                    posting.create()
            return posting
    def add(self):
        # Add the instance to the database
        db.session.add(self)
        db.session.commit()
        return self
    

    
def initPosting():
        with app.app_context():
            db.create_all()
            p1 = Posting(
                name='OCS',
                school='University of Washington',
                engineeringType='Computer engineering',
                partUsed='javascript, python',
                description='love coding and ocs, was an awesome project to work on'
            )
            p2 = Posting(
                name='Physics Boat',
                school='Northeastern',
                engineeringType='mechanical engineering',
                partUsed='wood, metal, plastic',
                description='learned to glue wood together'
            )
            posting = [p1, p2]
            for posting in posting:
                try:
                    posting.create()
                except IntegrityError:
                    '''Fails with bad or duplicate data'''
                    db.session.rollback()
