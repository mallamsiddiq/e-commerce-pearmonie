from . import create_app

# Create Flask app and Celery instance
app, celery = create_app()

if __name__ == '__main__':
    # Start the Celery worker
    celery.start()
