from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Tree:
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.date = data['date']
        self.zip = data['zip']
        self.notes = data['notes']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save_tree(cls, data):
        query = """
                INSERT INTO trees(species, location, date, zip, notes, users_id)
                VALUES(%(species)s, %(location)s, %(date)s, %(zip)s, %(notes)s, %(users_id)s);
                """
        return connectToMySQL('tree_info').query_db(query, data)
    
    @staticmethod
    def validate_tree(tree):
        is_valid = True
        if len(tree['species']) < 2:
            flash('Species must be at least 2 characters.')
            is_valid = False
        if len(tree['species']) < 1:
            flash('Species field required.')
            is_valid = False
        if len(tree['location']) < 5:
            flash('Location must be at least 5 characters.')
            is_valid = False
        if len(tree['location']) < 1:
            flash('Location field required.')
            is_valid = False
        if len(tree['notes']) > 49:
            flash('Notes must be less than 50 characters.')
            is_valid = False
        return is_valid
        
    @classmethod
    def get_all_w_creator(cls):
        query = "SELECT * FROM trees JOIN users WHERE users_id = users.id;"
        results = connectToMySQL('tree_info').query_db(query)

        all_trees = []

        if results:
            for row in results:
                tree = cls(row)
                data = {
                    'id' : row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                tree.creator = user.User(data)
                all_trees.append(tree)
        return all_trees
    
    @classmethod
    def get_tree_info(cls, data):
        query = "SELECT first_name, last_name FROM users JOIN trees WHERE trees.id = %(users.id)s"
        results = connectToMySQL('tree_info').query_db(query, data)

        return results

    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM trees WHERE id = %(id)s"

        result = connectToMySQL('tree_info').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET species=%(species)s, location=%(location)s, date=%(date)s, zip=%(zip)s, notes=%(notes)s"
        return connectToMySQL('tree_info').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trees WHERE id = %(id)s"
        return connectToMySQL('tree_info').query_db(query, data)