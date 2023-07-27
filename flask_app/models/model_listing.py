from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask import flash

DATABASE = "users_and_listings"

class Listing:
    def __init__(self, data):
        self.id = data['id']
        self.item = data['item']
        self.date = data['date']
        self.farm = data['farm']
        self.weight = data['weight']
        self.photo = data['photo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']



    def validate_listing(listing):
        is_valid = True
        if len(listing['item']) < 1:
            flash("All fields must be filled")
            is_valid = False

        if len(listing['farm']) < 1:
            flash("All fields must be filled")
            is_valid = False

        # if len(listing['date']) < 1:
        #     flash("All fields must be filled")
        #     is_valid = False

        if len(listing['weight']) < 0:
            flash("All fields must be filled")
            is_valid = False

        return is_valid
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM listings JOIN users ON listings.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        listings = []
        for entry in results:
            current_listing = cls(entry)
            user_info = {
                'id' : entry['users.id'],
                'first_name' : entry['first_name'],
                'last_name' : entry['last_name'],
                'email' : entry['email'],
                'password' : entry['password'],
                'photo' : entry['photo'],
                'created_at' : entry['users.created_at'],
                'updated_at' : entry['users.updated_at']
            }
            current_listing.user = model_user.User(user_info)
            listings.append(current_listing)
        return listings

    @classmethod
    def get_pic(cls):
        query = "SELECT photo FROM listings;"
        results = connectToMySQL(DATABASE).query_db(query)
        return results



    @classmethod
    def create(cls, data):
        query = "INSERT INTO listings (item, farm, date, weight, user_id, photo) VALUES (%(item)s, %(farm)s, %(date)s, %(weight)s, %(user_id)s, %(photo)s);"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results


    @classmethod
    def update(cls, data):
        query = "UPDATE listings SET item = %(item)s, farm = %(farm)s, date = %(date)s, weight = %(weight)s, photo = %(photo)s WHERE listings.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results 


    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM listings WHERE listings.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {'id':id})
        return results


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM listings JOIN users on users.id = listings.user_id WHERE listings.id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, {'id':id})
        if not result:
            return[]
        one_listing = result[0]
        instance_listing = cls(one_listing)
        if one_listing["users.id"] != None:
            user_data = {
                **one_listing,
                'id' : one_listing['users.id'],
                'created_at' : one_listing['users.created_at'],
                'updated_at' : one_listing['users.updated_at']
            }
            one_user = model_user.User(user_data)
            instance_listing.user = one_user
        return instance_listing