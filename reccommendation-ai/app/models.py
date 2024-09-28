from app import mongo
from datetime import datetime

# set interaction collection
product_interactions = mongo.db['user_product_interactions']
product_collection = mongo.db['product_collection']

def save_user_interaction(user_id, product_id, category):
    interaction = {
        'user_id': user_id,
        'product_id': product_id,
        'category': category,
        'created_at': datetime.utcnow()
    }
    product_interactions.insert_one(interaction)
    

def save_product_collection(product_name, product_id, category):
    collection = {
        'product_id': product_id,
        'product_name': product_name,
        'category': category,
        'created_at': datetime.utcnow()
    }
    product_collection.insert_one(collection)
    

def get_user_interactions():
    return list(product_interactions.find({}, {'_id':0}).sort('created_at', -1))

def get_product_collection():
    return list(product_collection.find({}, {'_id':0}).sort('created_at', -1))
    