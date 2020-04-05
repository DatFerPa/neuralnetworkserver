import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Maquinista, Turno


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='drop_tables')
@with_appcontext
def drop_tables():
    db.drop_all()

@click.command(name='generate_data')
@with_appcontext
def generate_data():
    #insertar datos para la bbdd
    a=1
