import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Maquinista, Turno, Admin


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
    turno1 = Turno(nombre_t="turno dia", maquina="mc 102023")
    turno2 = Turno(nombre_t="turno noche", maquina="23-405-5")
    turno3 = Turno(nombre_t="turno de explotacion",maquina="455-345-567")
    admin = Admin(nombre_admin="admin",password_admin="admin")
    maq1 = Maquinista(nombre_m="Fer")
    maq2 = Maquinista(nombre_m="Fernando")
    maq1.turnos.append(turno1)
    maq1.turnos.append(turno2)
    maq1.turnos.append(turno3)
    maq2.turnos.append(turno1)
    maq2.turnos.append(turno2)
    db.session.add(maq1)
    db.session.add(maq2)
    db.session.add(admin)
    db.session.commit()
