from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador


import os
import tempfile

import pytest

from control_turnos import control_turnos

@pytest.fixture
def client():
    db_fd, control_turnos.app.config['DATABASE'] = tempfile.mkstemp()
    control_turnos.app.config['TESTING'] = True

    with control_turnos.app.test_client() as client:
        with control_turnos.app.app_context():
            control_turnos.init_db()
        yield client

    os.close(db_fd)
    os.unlink(control_turnos.app.config['DATABASE'])



def test_operations_maquinista(client):
    maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
    db.session.add(maquinsta_prueba)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert maquinista is not None
    assert maquinista.nombre_m == "Maquinista1"
    db.session.delete(maquinista)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert maquinista is None


def test_operations_turno(client):
    turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
    db.session.add(turno_prueba)
    turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
    assert turno is not None
    assert turno.nombre_t == "Turno1"
    assert turno.maquina == "Maquina1"
    db.session.delete(turno)
    turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
    assert turno is None


def test_operations_asign_unasign(client):
    maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
    turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
    db.session.add(turno_prueba)
    db.session.add(maquinsta_prueba)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    tunro = Turno.query.filter_by(nombre_t="Turno1").first()
    maquinista.turnos.append(turno)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert len(maquinista.turnos) > 0
