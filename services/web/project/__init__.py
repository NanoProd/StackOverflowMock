from flask import Flask
from .extensions import *


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    app.config.from_object("project.config.Config")
    from project.app.views import views
    from project.app.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
