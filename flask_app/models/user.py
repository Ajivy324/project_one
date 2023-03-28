from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt 
from flask_app.models import sighting       
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sightings = []
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email, password, created_at, updated_at ) VALUES (%(fname)s , %(lname)s , %(email)s ,%(password)s, NOW() , NOW() );"
        results = connectToMySQL('Sasquatch_websighting').query_db( query, data )
        return results
    
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db(query, { "email" : email } )
        return cls(results[0]) if results else None
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db(query, { "id" : id } )
        return cls(results[0]) if results else None
    
    @classmethod
    def get_user_with_sighting(cls, data):
        query = "SELECT * FROM users LEFT JOIN sightings ON sightings.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('Sasquatch_websighting').query_db( query , data )
        print(results)
        user = cls( results[0])
        
        for db_row in results:
            sighting_data = {
                "id" : db_row["sighting.id"],
                "name" : db_row["sighting.name"],
                "descrip" : db_row["descrip"],
                "instructions" : db_row["instructions"],
                "under_30" : db_row["under_30"],
                "created_at" : db_row["sighting.created_at"],
                "updated_at" : db_row["sighting.updated_at"]
            }
            user.sightings.append( sighting.Sighting_data( sighting_data ))
        return user    


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['fname']) < 2:
            flash("first name must be at least 2 characters.", "registration")
            is_valid = False
        if len(user['lname']) < 2:
            flash("last name must be at least 2 characters.", "registration" )
            is_valid = False
        if User.get_by_email(user['email']):
            flash("Email already used", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "registration")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Your passwords don't match", "registration")
            is_valid = False
        if len(user['password']) < 8:
            flash("first name must be at least 8 characters.", "registration")
            is_valid = False
        return is_valid
    
        
