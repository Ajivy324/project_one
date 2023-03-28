from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app import app


class Sighting:
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happend =  data['what_happend']
        self.number_of = data['number_of']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created = None

    @classmethod
    def view(cls):
        query = "SELECT * FROM sightings JOIN users on users.id = sightings.user_id;"
        results = connectToMySQL('Sasquatch_websighting').query_db(query)
        sightings = []
        for sighting in results:
            one_sighting = cls(sighting)
            user_data = {
                "id" : sighting['users.id'],
                "first_name" : sighting["first_name"],
                "last_name" : sighting["last_name"],
                "email" : sighting["email"],
                "password" : '',
                "created_at" : sighting["users.created_at"],
                "updated_at" : sighting["users.updated_at"]
            }
            one_sighting.created = user.User(user_data)
            sightings.append(one_sighting )   
        return sightings
    @classmethod
    def get_one(cls, data):
        query =  "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db(query, data)
        return cls(results[0])
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO sightings ( location, what_happend, number_of, created_at, user_id ) VALUES (%(location)s , %(what_happend)s,%(number_of)s, %(created_at)s ,  %(user_id)s );"

        results = connectToMySQL('Sasquatch_websighting').query_db( query, data )
        return results
    @classmethod
    def view_one(cls, data):
        query =  "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE sightings SET location=%(location)s, what_happend=%(what_happend)s, number_of=%(number_of)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('Sasquatch_websighting').query_db(query,data)
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db( query, {"id": id}) 
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM sightings  JOIN users ON sightings.user_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db( query , data )
        if not results:
            return False
        results =  results[0]
        one_sighting = cls(results)
        user_data = {
            "id" : results["users.id"],
            "first_name" : results["first_name"],
            "last_name" : results["last_name"],
            "email" : results["email"],
            "password" : '',
            "created_at" : results["users.created_at"],
            "updated_at" : results["users.updated_at"]
        }
        one_sighting.created = user.User(user_data)
        return one_sighting    

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location']) < 3:
            flash("name must be at least 3 characters.", "new")
            is_valid = False
        if len(sighting['what_happend']) < 3:
            flash("description must be at least 3 characters.", "new" )
            is_valid = False
        if sighting["created_at"] == '':
            flash("please add date", "new")
        if sighting["number_of"] < '1':
            flash("must not be less then 1", "new")
        return is_valid
    
    @staticmethod
    def validate_update(sighting):
        is_valid = True
        if len(sighting['location']) < 3:
            flash("name must be at least 3 characters.", "new")
            is_valid = False
        if len(sighting['what_happend']) < 3:
            flash("description must be at least 3 characters.", "new" )
            is_valid = False
        if sighting["updated_at"] == '':
            flash("Please Add Date", "new")
        if sighting["number_of"] < '1':
            flash("must not be less then 1", "new")
        return is_valid
