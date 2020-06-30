import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Maquinista, Turno, Administrador
"""
from tests.test_pruebasBBDD import *

@click.command(name="make_tests")
@with_appcontext
def make_tests():
    test_operations_maquinista()
    test_operaciones_negativas_maquinista()
    test_operations_turno()
    test_operaciones_negativas_turno()
    test_operations_asign_unasign()
"""
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
    admin = Administrador(nombre_admin="admin",password_admin="admin")
    maq1 = Maquinista(nombre_m="Fer")
    maq2 = Maquinista(nombre_m="Fernando")

    maq3 = Maquinista(nombre_m="Federico Garcia")
    maq4 = Maquinista(nombre_m="Jose Coronado")
    maq5 = Maquinista(nombre_m="Pepin Tre")
    maq6 = Maquinista(nombre_m="Antonio Valdomero")
    maq7 = Maquinista(nombre_m="Susana Alcacia")
    maq8 = Maquinista(nombre_m="Lupita Arsenio")

    turn1 = Turno(nombre_t="turno direccion Gijon",maquina="141-2001")
    turn2 = Turno(nombre_t="turno direccion Lugones",maquina="141-2001")
    turn3 = Turno(nombre_t="turno hacia Siero",maquina="240-2471")
    turn4 = Turno(nombre_t="turno sin retorno",maquina="481-27-3")
    turn5 = Turno(nombre_t="mercancias destileria",maquina="777-312")
    turn6 = Turno(nombre_t="mercancias hierros",maquina="555A-15")
    turn7 = Turno(nombre_t="Paseo por el lago",maquina="1-2-3")

    maq3.turnos.append(turn1)
    maq3.turnos.append(turn2)
    maq3.turnos.append(turn3)

    maq4.turnos.append(turn5)
    maq4.turnos.append(turn6)

    maq5.turnos.append(turn7)
    maq5.turnos.append(turn4)
    maq5.turnos.append(turn2)

    maq6.turnos.append(turn3)
    maq6.turnos.append(turn7)
    maq6.turnos.append(turn1)

    maq7.turnos.append(turn1)
    maq7.turnos.append(turn2)
    maq7.turnos.append(turn3)
    maq7.turnos.append(turn4)

    maq8.turnos.append(turn5)
    maq8.turnos.append(turn6)

    maq1.turnos.append(turno1)
    maq1.turnos.append(turno2)
    maq1.turnos.append(turno3)
    maq2.turnos.append(turno1)
    maq2.turnos.append(turno2)
    db.session.add(maq1)
    db.session.add(maq2)
    db.session.add(maq3)
    db.session.add(maq4)
    db.session.add(maq5)
    db.session.add(maq6)
    db.session.add(maq7)
    db.session.add(maq8)
    db.session.add(admin)
    db.session.commit()
