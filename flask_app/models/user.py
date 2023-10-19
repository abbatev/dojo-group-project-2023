from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "dojo_cars"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # Inserts data from form into users table in database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    # Selects user based on email. Used to verify whether email is already in use or not in the database
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Selects user based on id. Used to verify if a particular user was the creator of a specific sighting
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    # Used to validated registration of user and prepares messages to be flashed for any missing elements
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['email']) < 1:
            flash("Email must not be blank", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Email is invalid", "register")
            is_valid = False
        elif User.get_by_email(data):
            flash("Email already in use", "register")
            is_valid = False
        if len(data['first_name']) < 1:
            flash("First name must not be blank", "register")
            is_valid = False
        elif len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name must not be blank", "register")
            is_valid = False
        elif len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(data['first_name']) < 1:
            flash("Password must not be blank", "register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if data['confirm_password'] != data['password']:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid
