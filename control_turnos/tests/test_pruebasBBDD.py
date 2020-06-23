import pytest
from .extensions import db
from .models import Maquinista, Turno, Administrador

def test_operations_maquinista():
    maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
    db.session.add(maquinsta_prueba)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert maquinista is not None
    assert maquinista.nombre_m == "Maquinista1"
    db.session.delete(maquinista)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert maquinista is None


def test_operations_turno():
    turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
    db.session.add(turno_prueba)
    turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
    assert turno is not None
    assert turno.nombre_t == "Turno1"
    assert turno.maquina == "Maquina1"
    db.session.delete(turno)
    turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
    assert turno is None

def test_operations_asign_unasign():
    maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
    turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
    db.session.add(turno_prueba)
    db.session.add(maquinsta_prueba)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    tunro = Turno.query.filter_by(nombre_t="Turno1").first()
    maquinista.turnos.append(turno)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    assert len(maquinista.turnos) > 0

    
