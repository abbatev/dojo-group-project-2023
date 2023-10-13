from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, listing
from flask import flash

class Comment:
    db = "dojo_cars"
    def __init__(self,data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.listing_id = data["listing_id"]
        self.commenter = None

        @classmethod
        def save(cls, data):
            query = "INSERT INTO comments (id, content, created_at, user_id, listing_id) VALUES (%(id)s, %(content)s, NOW(), %(user_id)s, %(listing_id)s);"
            return connectToMySQL(cls.db).query_db(query,data)

        @classmethod
        def get_comments_for_listing(cls,data):
            query = "SELECT * FROM comments JOIN users on comments.user_id = users.id JOIN comments.listing_id = listings.id WHERE comments.listing_id = %(id)s"
            results = connectToMySQL(cls.db).query_db(query,data)
            this_listing_comments = []
            for row in results:
                this_comment = cls(row)
                user_data = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": "",
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                this_comment.commenter = user.User(user_data)
                this_listing_comments.append(this_comment)
            return this_listing_comments

        # Deletes row in sightings table
        @classmethod
        def destroy(cls,data):
            query = "DELETE FROM comments WHERE id = %(id)s;"
            return connectToMySQL(cls.db).query_db(query,data)