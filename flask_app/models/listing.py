from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment
from flask import flash

class Listing:
    db = "dojo_cars"
    def __init__(self,data):
        self.id = data["id"]
        self.make_model = data["make_model"]
        self.year = data["year"]
        self.condition = data["condition"]
        self.price = data["price"]
        self.mileage = data["mileage"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.seller = None

    # Inserts data from form into listings table in database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO listings (make_model, `condition`, year, price, mileage, description, created_at, user_id) VALUES (%(make_model)s, %(condition)s, %(year)s, %(price)s, %(mileage)s, %(description)s, NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    # Selects all listings from database with their associated seller to be displayed on the dashboard
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM listings JOIN users ON listings.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_listings = []
        for row in results:
            this_listing = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_listing.seller = user.User(user_data)
            all_listings.append(this_listing)
        return all_listings

    # Selects single listing with associated seller by id. This is used to verify if a user has access to edit and delete the listing as well as to view individual listings
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM listings JOIN users ON listings.user_id = users.id WHERE listings.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False
        result = result[0]
        this_listing = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
            }
        this_listing.seller = user.User(user_data)
        return this_listing

    # Update row in listings table identified by listing id
    @classmethod
    def update(cls,data):
        query = "UPDATE listings SET make_model = %(make_model)s, `condition` = %(condition)s, year = %(year)s, price = %(price)s, mileage = %(mileage)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # Deletes row in listings table identified by listing id
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM listings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # Validates creation of listing ot make sure all information is filled in
    @staticmethod
    def validate_listing(data):
        is_valid = True
        if len(data['make_model']) < 1:
            flash("Make and Model are required")
            is_valid = False
        if len(str(data['year'])) !=4:
            flash("Year is required")
            is_valid = False
        elif int(data['year']) < 1900 or int(data['year']) > 2024:
            flash("Year is out of range")
            is_valid = False
        if len(data['description']) < 1:
            flash("Description is required")
            is_valid = False
        if len(data['condition']) < 1:
            flash("Condition is required")
            is_valid = False
        if not data['price']:
            flash("Price is required")
            is_valid = False
        if not data['mileage']:
            flash("Mileage is required")
            is_valid = False
        return is_valid
