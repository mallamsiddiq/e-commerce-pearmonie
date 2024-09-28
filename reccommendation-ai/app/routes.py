from flask import Blueprint, request, jsonify, Response
from app.services import plain_cat_model, user_interaction_model
from datetime import datetime
from bson.json_util import dumps
from app.models import (save_user_interaction, get_user_interactions, 
                        save_product_collection, get_product_collection, 
                        product_collection)


recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/interaction-recommendations', methods=['GET'])
def get_interaction_recommendations():
    product_id = request.args.get('product_id')
    category = request.args.get('category') 
    offset = request.args.get('offset')

    if not product_id or not category:
        return jsonify({'error': 'Missing product_id or category'}), 400

    recommended_product_ids = user_interaction_model.recommend_products(product_id, category)
    
    # Query MongoDB using recommended product IDs
    recommended_products = product_collection.find({
        "product_id": {"$in": recommended_product_ids}
    })

    recommended_products_list = list(recommended_products)

    # Serialize the result to JSON
    response = dumps(recommended_products_list)

    return Response(response, mimetype='application/json')


@recommendation_bp.route('/category-recommendations', methods=['GET'])
def get_category_recommendations():
    category = request.args.get('category') 
    offset = request.args.get('offset')

    if not category:
        return jsonify({'error': 'Missing category'}), 400

    # Get recommended product IDs from the model
    recommended_product_ids = plain_cat_model.recommend_products(category)

    # Query MongoDB using recommended product IDs
    recommended_products = product_collection.find({
        "product_id": {"$in": recommended_product_ids}
    })

    recommended_products_list = list(recommended_products)

    # Serialize the result to JSON
    response = dumps(recommended_products_list)

    return Response(response, mimetype='application/json')


@recommendation_bp.route('/interactions', methods=['POST'])
def save_interaction():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    category = data.get('category')

    if not user_id or not product_id or not category:
        return jsonify({'error': 'user_id, product_id, and category are required'}), 400

    save_user_interaction(user_id, product_id, category)
    
    return jsonify({'message': 'Interaction saved successfully'}), 201


@recommendation_bp.route('/interactions', methods=['GET'])
def get_interactions():

    # Assuming get_interactions is a function that retrieves interactions from a database
    interactions = get_user_interactions()

    if not interactions:
        return jsonify({'message': 'No interactions found'}), 404
    
    return jsonify({'interactions': interactions}), 200


@recommendation_bp.route('/products', methods=['POST'])
def seed_products():
    data = request.json
    product_name = data.get('product_name')
    product_id = data.get('product_id')
    category = data.get('category')

    if not product_name or not product_id or not category:
        return jsonify({'error': 'product_name, product_id, and category are required'}), 400

    save_product_collection(product_name, product_id, category)
    
    return jsonify({'message': 'Product saved successfully'}), 201


@recommendation_bp.route('/products', methods=['GET'])
def get_all_products():

    # Assuming get_interactions is a function that retrieves interactions from a database
    products = get_product_collection()

    if not products:
        return jsonify({'message': 'No products found'}), 404
    
    return jsonify({'products': products}), 200
