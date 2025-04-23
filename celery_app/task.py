from celery_app import app
import time

@app.task(name='tasks.django_task')
def django_task():
    """
    A simple Celery task that prints a message.
    """
    print("This is a Django task running in Celery.")
    time.sleep(5)
    print("Django task completed.")
    return "Django task completed."

@app.task(name='tasks.flask_task')
def flask_task():
    """
    A simple Celery task that prints a message.
    """
    print("This is a Flask task running in Celery.")
    time.sleep(5)
    print("Flask task completed.")
    return "Flask task completed."