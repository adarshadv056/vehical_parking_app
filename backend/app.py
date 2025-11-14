from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from models.models import db, user
import os
from flask_caching import Cache
from applications.celery_init import celery_init_app
from celery.schedules import crontab

app = None
jwt = JWTManager()
cache = Cache()

def parking_app():
    global app
    app = Flask(__name__, static_folder='application/static', static_url_path='/static')
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    
    app.debug = True
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    app.app_context().push()

def create_admin_with_db():
    if not os.path.exists('parking.db'):
        db.create_all()
        if not user.query.filter_by(username='Admin').first():
            admin = user(
                username='Admin',
                email='admin@gmail',
                password=generate_password_hash('admin123'),
                address='Admin Office',
                pincode='', role='admin'
                )
            db.session.add(admin)
            db.session.commit()

parking_app()
create_admin_with_db()
celery = celery_init_app(app)
celery.autodiscover_tasks()

from routes.routes import *

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab('*/1'), # every minute
        # crontab(0, 0, day_of_month='1'),
        monthly_activity_report.s(),
        name='monthly_activity_report'
    )
    
    sender.add_periodic_task(
        crontab('*/1'),
        # crontab(hour=8, minute=0), # every day at 8 AM
        daily_reminder.s(),
        name='daily_reminder'
    )

if __name__ == '__main__':
    app.run()