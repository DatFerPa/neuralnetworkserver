from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador


def test_operations_maquinista():
    print('operaciones con los maquinistas')
    try:
        maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
        db.session.add(maquinsta_prueba)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        assert maquinista is not None
        assert maquinista.nombre_m == "Maquinista1"
        db.session.delete(maquinista)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        assert maquinista is not None
    except AssertionError as error:
        print('Fallo en el Test operaciones con los maquinistas')
        print(error)

def test_operaciones_negativas_maquinista():
    print('operaciones negativas con los maquinsitas')
    try:
        maquinista_1 = Maquinista(nombre_m="Maquinista1")
        db.session.add(maquinista_1)
        maquinista_2 = Maquinista(nombre_m="maquinista1")
        db.session.add(maquinista_2)
        maquinistas = Maquinista.query.filter_by(nombre_m="Maquinista1").all()
        assert len(maquinistas) == 1
    except AssertionError as error:
        print('Fallo en el Test operaciones negativas con los maquinistas')
        print(error)

def test_operations_turno():
    print('operaciones con los turnos')
    try:
        turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_prueba)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        assert turno is not None
        assert turno.nombre_t == "Turno1"
        assert turno.maquina == "Maquina1"
        db.session.delete(turno)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        assert turno is None
    except AssertionError as error:
        print('Fallo en el Test operaciones con los turnos')
        print(error)

def test_operaciones_negativas_turno():
    print('operaciones negativas con los turnos')
    try:
        turno_1 = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_1)
        turno_2 = Turno(nombre_t="Turno1",maquina="Maquina1")
        dab.session.add(turno_2)
        turnos = Turno.query.filter_by(nombre_t="Turno1").all()
        assert len(turnos) == 1
    except AssertionError as error:
        print('Fallo en el Test operaciones negativas con los turnos')


def test_operations_asign_unasign():
    maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
    turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
    db.session.add(turno_prueba)
    db.session.add(maquinsta_prueba)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    tunro = Turno.query.filter_by(nombre_t="Turno1").first()
    maquinista.turnos.append(turno)
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    #append
    assert len(maquinista.turnos) > 0
    maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
    cont = 0
    for turn in maquinista.turnos:
        if turn.nombre_t == "Turno1":
            maquinista.turnos.pop(cont)
        cont += 1
    assert len(maquinista.turnos) == 0
    except AssertionError as error:
        print('Fallo en el Test de operaciones asignar y desasignar')
