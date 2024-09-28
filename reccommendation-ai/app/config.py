import os 
class Config:
    MONGO_URI = 'mongodb://mongo:27017/your_database_name'
    CLIENT_HEADER_SECRET = os.environ.get('CLIENT_HEADER_SECRET')
    
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    
    broker_url = 'redis://redis:6379/0'
    result_backend = 'redis://redis:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Asia/Kolkata'
    enable_utc = True


app_config = {
    'config': Config
}

