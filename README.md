
## E  commerce microservie api


## Store and Product API Documentation

### Overview

This API allows users to manage stores and products within those stores. Users can create, update, retrieve, and delete stores and products. Additionally, it includes features for viewing the most popular products and tracking product views.



## Flask AI Recommendation Service Documentation

### Overview

The Flask AI Recommendation Service provides personalized product recommendations for an eCommerce platform. It leverages machine learning models to analyze user interactions and product categories, thereby enhancing user experience through tailored suggestions. This service is designed to receive asynchronous updates from the eCommerce service, allowing it to maintain up-to-date data for accurate recommendations.

the main service is hosted on port 8000 while the recommendatio api is hosted on port 5001 
### Authentication

All API requests require authentication. Users must obtain a token via an authentication process and include it in the headers of their requests:

#### Authentication Header
```plaintext
Authorization: Token <your_token_here>
```

### API Endpoints

#### 1. Store Endpoints

###### Base URL
```
/api/v1/store/
```

###### 1.1. List Stores
**GET** `/api/v1/store/`

**Description:** Retrieves a list of stores. Admins can view all stores, while regular users can only view their own.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Store Name",
        "owner": "Owner Username"
    },
    ...
]
```

###### 1.2. Retrieve a Store
**GET** `/api/v1/store/{id}/`

**Description:** Retrieves details of a specific store.

**Response:**
```json
{
    "id": 1,
    "name": "Store Name",
    "owner": "Owner Username"
}
```

###### 1.3. Create a Store
**POST** `/api/v1/store/`

**Description:** Creates a new store. The owner is automatically set to the authenticated user.

**Request Body:**
```json
{
    "name": "New Store Name"
}
```

**Response:**
```json
{
    "id": 2,
    "name": "New Store Name",
    "owner": "Owner Username"
}
```

###### 1.4. Update a Store
**PUT** `/api/v1/store/{id}/`

**Description:** Updates the details of a specific store.

**Request Body:**
```json
{
    "name": "Updated Store Name"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Updated Store Name",
    "owner": "Owner Username"
}
```

###### 1.5. Delete a Store
**DELETE** `/api/v1/store/{id}/`

**Description:** Deletes a specific store.

**Response:**
```json
{
    "detail": "Store deleted successfully."
}
```

#### 2. Product Endpoints

###### Base URL
```
/api/v1/store/products/
```

###### 2.1. List Products
**GET** `/api/v1/store/products/`

**Description:** Retrieves a list of products. Admins can view all products, while regular users can only view products from their own stores.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Product Name",
        "description": "Product Description",
        "price": "10.00",
        "quantity": 100,
        "category": "Category Name",
        "store": 1,
        "views_count": 5,
        "converted_price": "10.00"
    },
    ...
]
```

###### 2.2. Retrieve a Product
**GET** `/api/v1/store/products/{id}/`

**Description:** Retrieves details of a specific product.

**Response:**
```json
{
    "id": 1,
    "name": "Product Name",
    "description": "Product Description",
    "price": "10.00",
    "quantity": 100,
    "category": "Category Name",
    "store": 1,
    "views_count": 5,
    "converted_price": "10.00"
}
```

###### 2.3. Create a Product
**POST** `/api/v1/store/products/`

**Description:** Creates a new product within a store. The store is identified by `store_id`.

**Request Body:**
```json
{
    "name": "New Product",
    "description": "Product Description",
    "price": "10.00",
    "quantity": 100,
    "category": "Category Name",
    "store_id": 1
}
```

**Response:**
```json
{
    "id": 2,
    "name": "New Product",
    "description": "Product Description",
    "price": "10.00",
    "quantity": 100,
    "category": "Category Name",
    "store": 1,
    "views_count": 0,
    "converted_price": "10.00"
}
```

###### 2.4. Update a Product
**PUT** `/api/v1/store/products/{id}/`

**Description:** Updates the details of a specific product.

**Request Body:**
```json
{
    "name": "Updated Product",
    "description": "Updated Description",
    "price": "12.00",
    "quantity": 150,
    "category": "Updated Category"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Updated Product",
    "description": "Updated Description",
    "price": "12.00",
    "quantity": 150,
    "category": "Updated Category",
    "store": 1,
    "views_count": 5,
    "converted_price": "12.00"
}
```

###### 2.5. Delete a Product
**DELETE** `/api/v1/store/products/{id}/`

**Description:** Deletes a specific product.

**Response:**
```json
{
    "detail": "Product deleted successfully."
}
```

###### 2.6. View Most Popular Products
**GET** `/api/v1/store/products/most-popular/`

**Description:** Retrieves a list of the most popular products based on view count.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Popular Product",
        "description": "Product Description",
        "price": "10.00",
        "quantity": 100,
        "category": "Category Name",
        "store": 1,
        "views_count": 100,
        "converted_price": "10.00"
    },
    ...
]
```

#### 3. View Product Details and Increment Views
**GET** `/api/v1/store/products/{id}/`

**Description:** Retrieves the details of a product and increments its view count for the authenticated user.

**Response:**
```json
{
    "id": 1,
    "name": "Product Name",
    "description": "Product Description",
    "price": "10.00",
    "quantity": 100,
    "category": "Category Name",
    "store": 1,
    "views_count": 1,  # Incremented
    "converted_price": "10.00"
}
```

### Error Handling

In case of an error, the API will respond with a 4xx or 5xx status code along with an error message. Example error responses include:

- **Validation Error (400)**
```json
{
    "detail": "No store available for this user. Admins must provide a store explicitly."
}
```

- **Permission Denied (403)**
```json
{
    "detail": "Only store owners or Admins can add product to store."
}
```

### Example Usage

#### Fetching Stores
```bash
curl -H "Authorization: Token <your_token_here>" -X GET http://localhost:8000/api/v1/store/
```

#### Creating a Product
```bash
curl -H "Authorization: Token <your_token_here>" -X POST http://localhost:8000/api/v1/store/products/ \
-H "Content-Type: application/json" \
-d '{"name": "New Product", "description": "Product Description", "price": "10.00", "quantity": 100, "category": "Category Name", "store_id": 1}'
```

### Conclusion

This API provides a comprehensive solution for managing stores and products in your application. By following the provided documentation, you can easily integrate the API into your front-end application or use it for other purposes. For any issues or additional features, please refer to the source code or contact the development team.


# Flask AI Recommendation Service Documentation

### Features

- **Category-Based Recommendations:** Utilizes K-Means clustering for product recommendations based on their categories.
- **User Interaction Recommendations:** Implements a K-Nearest Neighbors (KNN) model to suggest products based on user interactions.
- **Asynchronous Data Updates:** Supports real-time updates from the eCommerce service to ensure the recommendation models use the latest product and interaction data.
- **Periodic Model Training:** The service periodically retrains the recommendation models using the most recent data to improve recommendation accuracy and adapt to changing user preferences.

### Model Training

#### 1. Periodic Training

The models are trained periodically to ensure they reflect the latest product interactions and user behavior. The periodic training is crucial for maintaining the relevance and accuracy of recommendations. The training schedule can be configured based on the frequency of data updates and system performance considerations.

#### 2. Category-Based Model

- **Model Path:** `ai-models/plain_category_fit_model.pkl`
- **Function:** `train_model(model_path='ai-models/plain_category_fit_model.pkl', num_clusters=5)`
  - Retrieves product data from MongoDB.
  - Vectorizes product categories using `TfidfVectorizer`.
  - Trains a K-Means model and saves it with `joblib`.

#### 3. User Interaction Model

- **Model Path:** `ai-models/user_cat_interaction_model.pkl`
- **Function:** `train_model(model_path='ai-models/user_cat_interaction_model.pkl')`
  - Collects user-product interaction data from MongoDB.
  - Constructs a user-product interaction matrix.
  - Trains a KNN model and saves it along with the interaction matrix.

### API Endpoints

#### 1. Interaction Recommendations

- **Endpoint:** `GET /interaction-recommendations`
- **Description:** Provides product recommendations based on user interactions.
- **Parameters:**
  - `product_id`: ID of the product to base recommendations on.
  - `category`: Category of the product.
- **Response:**
  - Returns a list of recommended product IDs.
  
###### Example Request:
```
GET /interaction-recommendations?product_id=123&category=Electronics
```

#### 2. Category Recommendations

- **Endpoint:** `GET /category-recommendations`
- **Description:** Provides product recommendations based on category.
- **Parameters:**
  - `category`: The category for which recommendations are sought.
- **Response:**
  - Returns a list of recommended product IDs.
  
###### Example Request:
```
GET /category-recommendations?category=Electronics
```

#### 3. Save User Interaction

- **Endpoint:** `POST /interactions`
- **Description:** Saves user interaction data to the database. This endpoint is primarily used by the eCommerce service to send user interaction updates asynchronously.
- **Request Body:**
  - `user_id`: ID of the user.
  - `product_id`: ID of the product interacted with.
  - `category`: Category of the product.
- **Response:**
  - Confirms successful saving of interaction data.

###### Example Request:
```json
POST /interactions
{
  "user_id": "user123",
  "product_id": "product456",
  "category": "Electronics"
}
```

#### 4. Get User Interactions

- **Endpoint:** `GET /interactions`
- **Description:** Retrieves all user interactions from the database.
- **Response:**
  - Returns a list of user interactions.

###### Example Request:
```
GET /interactions
```

#### 5. Seed Products

- **Endpoint:** `POST /products`
- **Description:** Saves a new product to the product collection. This endpoint is used by the eCommerce service to add products asynchronously.
- **Request Body:**
  - `product_name`: Name of the product.
  - `product_id`: ID of the product.
  - `category`: Category of the product.
- **Response:**
  - Confirms successful saving of the product.

###### Example Request:
```json
POST /products
{
  "product_name": "Smartphone",
  "product_id": "product789",
  "category": "Electronics"
}
```

#### 6. Get All Products

- **Endpoint:** `GET /products`
- **Description:** Retrieves all products from the product collection.
- **Response:**
  - Returns a list of products.

###### Example Request:
```
GET /products
```

### Access Control

To ensure security and proper access management, the Flask AI Recommendation Service restricts access to certain endpoints:

- **Public Endpoints:** 
  - The following endpoints are publicly accessible:
    - `/interaction-recommendations`
    - `/category-recommendations`
  
- **Protected Endpoints:** 
  - All other endpoints require a valid token for access, as they are intended for internal use by the eCommerce service. Requests to these endpoints must include a token in the `CLIENT_HEADER_SECRET` header. I have provided in the environment for seamless communication

#### Token Middleware

The service implements a token middleware to enforce access control:

```python

class TokenMiddleware:
    
```

### Asynchronous Integration

The Flask AI Recommendation Service is designed endpoints to listen for updates from the eCommerce service, which includes:

#### 1. User Interactions

- **Endpoint:** `POST /ai/interactions`
  - This endpoint allows the eCommerce service to send user interaction data asynchronously, ensuring that the recommendation system has access to the latest interaction information for generating personalized recommendations.

#### 2. Product Updates

- **Endpoint:** `POST /ai/products`
  - This endpoint enables the eCommerce service to add new products to the recommendation system without blocking other operations. This ensures that the product catalog remains current and can be utilized for recommendations immediately.

### Conclusion

The Flask AI Recommendation Service provides a robust framework for delivering personalized product recommendations in an eCommerce context. With its integration of machine learning models, periodic training, and support for asynchronous updates from the eCommerce service, this system offers a dynamic and efficient way to enhance user experience. Use the provided API endpoints to utilize the recommendation capabilities effectively.