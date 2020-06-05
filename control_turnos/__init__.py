from flask import Flask
from .commands import create_tables, drop_tables, generate_data
from .extensions import db, login_manager
from .routes.androidRoutes import androidRoutes
from .routes.webRoutes import webRoutes
from .models import Administrador


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret_key_que_jamas_se_adivinará$¿?'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT']= False

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'webRoutes.principal'

    @login_manager.user_loader
    def load_user(user_id):
        return Administrador.query.get(id = user_id).first()

    app.register_blueprint(androidRoutes)
    app.register_blueprint(webRoutes)


    app.cli.add_command(create_tables)
    app.cli.add_command(drop_tables)
    app.cli.add_command(generate_data)

    return app
