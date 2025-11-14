from celery import Celery, Task
from flask import Flask
# import applications.task
# from applications.celery_init import celery

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('celery_config')
    # celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app

# flask_app = Flask(__name__)
# flask_app.config.from_object('celery_config')

# celery = celery_init_app(flask_app)