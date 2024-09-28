from flask import Flask
from flask_pymongo import PyMongo
from .middlewares import TokenMiddleware
from .config import Config
from celery import Celery
from celery.schedules import crontab


app = Flask(__name__)
mongo = PyMongo()

def create_app():    
    # Load configuration
    app.config.from_object(Config)

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize Celery with app context
    celery = make_celery(app)
    
    app.wsgi_app = TokenMiddleware(app.wsgi_app)

    # Register blueprints (routes)
    register_blueprints(app)

    return app, celery  # Return both the Flask app and Celery instance


def register_blueprints(app):
    # Import and register all Blueprints
    from .routes import recommendation_bp
    app.register_blueprint(recommendation_bp, url_prefix='/ai')
    
def make_celery(app):
    celery = Celery()
    celery.config_from_object(Config)
    # celery.conf.update(app.config)
    
    celery.conf.beat_schedule = {
        'train_category_model_task_midnight': {
            'task': 'train_category_model_task',
            'schedule': crontab(hour=0, minute=0),  # Run at midnight every day
        },
        'train_category_model_task_30': {
            'task': 'train_category_model_task',
            'schedule': 30,
        },
        'train_interaction_model_task_midnight': {
            'task': 'train_interaction_model_task',
            'schedule': crontab(hour=1, minute=0),  # Run at midnight every day
        },
        'train_interaction_model_task_30': {
            'task': 'train_interaction_model_task',
            'schedule': 35,
        },
    }

    # Ensure tasks have access to Flask context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            

    celery.Task = ContextTask
    celery.autodiscover_tasks(['app.tasks'])

    return celery


