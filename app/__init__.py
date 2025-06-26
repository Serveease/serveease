from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
import os

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'serveeaseatyourservice'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serveease.db'
    load_dotenv()
    
    app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')
    app.config['PREFFERED_URL_SCHEME'] = 'https'
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth_routes import auth
    from .routes.main_routes import main
    from .routes.request_routes import request_bp
    from .routes.appointment_routes import appointment
    from .routes.payment_routes import payment
    from .routes.feedback_routes import feedback
    from .routes.file_routes import file_routes
    from .routes.announcement_routes import announcement
    from .routes.admin_routes import admin
    from .routes.service_routes import service_bp
    from .routes.request_routes import request_bp
    from app.routes.track_routes import track_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(appointment)
    app.register_blueprint(payment)
    app.register_blueprint(feedback)
    app.register_blueprint(file_routes)
    app.register_blueprint(announcement)
    app.register_blueprint(admin)
    app.register_blueprint(service_bp)
    app.register_blueprint(request_bp)  
    app.register_blueprint(track_bp)

    


    return app
