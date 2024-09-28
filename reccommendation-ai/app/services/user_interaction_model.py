import pandas as pd, os, joblib
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from app.models import product_interactions

model_path = 'ai-models/user_cat_intaraction_model.pkl'

def train_model(model_path=model_path):
    interactions = product_interactions.find()
    
    # Create DataFrame for user-product interactions
    data = pd.DataFrame(list(interactions))
    if data.empty:
        print("No interaction data found.")
        return
    
    # Create user-product interaction matrix (sparse format)
    user_product_matrix = data.pivot_table(index='product_id', columns='user_id', aggfunc='size', fill_value=0)
    user_product_matrix_sparse = csr_matrix(user_product_matrix)
    
    # Train KNN model using sparse matrix
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(user_product_matrix_sparse)
    
    # Save the model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    joblib.dump({'model': model, 'matrix': user_product_matrix}, model_path) # Save model with matrix


def recommend_products(product_id, category, n_recommendations=5):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file {model_path} does not exist. Train the model first.")
    
    # Load model and matrix
    model_data = joblib.load(model_path)
    model = model_data['model']
    user_product_matrix = model_data['matrix']
   
    
    # # Ensure product exists in the filtered matrix
    if product_id not in user_product_matrix.index:
        return []
        
    # Find index of the product in the original matrix
    user_index = user_product_matrix.index.get_loc(product_id)
    
    # Reshape product interaction vector to pass to the model
    product_vector = csr_matrix(user_product_matrix.iloc[user_index, :].values.reshape(1, -1))
    
    # Adjust n_neighbors to avoid exceeding available samples
    n_samples_fit = user_product_matrix.shape[0]
    adjusted_n_neighbors = min(n_recommendations + 1, n_samples_fit)  # Ensure n_neighbors <= n_samples_fit

    # Predict nearest neighbors
    distances, indices = model.kneighbors(product_vector, n_neighbors=adjusted_n_neighbors)
    
    # Get recommended product IDs, excluding the input product itself
    recommended_product_ids = user_product_matrix.index[indices.flatten()[1:]].tolist()
    
    return recommended_product_ids if recommended_product_ids else []
