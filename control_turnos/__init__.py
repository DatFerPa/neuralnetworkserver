from flask import Flask

from .commands import create_tables, drop_tables, generate_data
from .extensions import db
from .routes.androidRoutes import androidRoutes
from .routes.webRoutes import webRoutes


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(androidRoutes)
    app.register_blueprint(webRoutes)


    app.cli.add_command(create_tables)
    app.cli.add_command(drop_tables)
    app.cli.add_command(generate_data)

    return app
