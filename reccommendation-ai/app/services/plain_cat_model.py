import pandas as pd, os, joblib
from sklearn.cluster import KMeans

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from app.models import product_collection

def train_model(model_path='ai-models/plain_category_fit_model.pkl', num_clusters=5):
    # Connect to MongoDB
    
    collection = product_collection
    
    # Fetch product data from MongoDB
    data = pd.DataFrame(list(collection.find()))
    
    # Extract the 'id' and 'category' fields
    product_data = data[['product_id', 'category']].dropna()

    # Vectorize the 'category' field
    vectorizer = TfidfVectorizer()
    category_matrix = vectorizer.fit_transform(product_data['category'])

    # Train the K-Means model
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(category_matrix)
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the trained model and vectorizer using joblib
    joblib.dump({'model': kmeans, 'vectorizer': vectorizer}, model_path)
    
def recommend_products(category, model_path='ai-models/plain_category_fit_model.pkl'):
    # Load the trained model and vectorizer
    model_data = joblib.load(model_path)
    kmeans = model_data['model']
    vectorizer = model_data['vectorizer']
    
    collection = collection = product_collection
    
    # Fetch product data from MongoDB
    data = pd.DataFrame(list(collection.find()))
    product_data = data[['product_id', 'category']].dropna()
    
    # Get the category of the selected product
    selected_category = category
    
    # Vectorize the category of the selected product
    category_vector = vectorizer.transform([selected_category])
    
    # Predict the cluster for the selected product
    selected_cluster = kmeans.predict(category_vector)[0]
    
    # Find other products in the same cluster
    product_data['cluster'] = kmeans.predict(vectorizer.transform(product_data['category']))
    recommended_products = product_data[product_data['cluster'] == selected_cluster]

    return  recommended_products['product_id'].tolist()