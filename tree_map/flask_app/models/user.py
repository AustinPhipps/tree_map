from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import tree
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users(first_name, last_name, email, password)
                    VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        
        return connectToMySQL('tree_info').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('Names must be at least 2 characters long.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Names must be at least 2 characters long.')
            is_valid = False
        if not EMAIL_REGEX.match (user['email']):
            flash('Email must be in valid email format.')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Password and confirm password must match.')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('tree_info').query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])