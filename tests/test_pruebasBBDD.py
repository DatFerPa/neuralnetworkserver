from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador


def test_operations_maquinista():
    print('Operaciones con los maquinistas')
    try:
        maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
        db.session.add(maquinsta_prueba)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        assert maquinista is not None, "El maquinista no se ha añadido correctamente"
        assert maquinista.nombre_m == "Maquinista1", "Información del maquinsita incorrecta"
        db.session.delete(maquinista)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        assert maquinista is None,"El maquinista no se ha eliminado adecuadamente"
        print('Exito en operaciones con los maquinistas')
    except AssertionError as error:
        print('Fallo en el Test operaciones con los maquinistas')
        print(error)

def test_operaciones_negativas_maquinista():
    print('Operaciones negativas con los maquinsitas')
    try:
        maquinista_1 = Maquinista(nombre_m="Maquinista1")
        db.session.add(maquinista_1)
        try:
            maquinista_2 = Maquinista(nombre_m="Maquinista1")
            db.session.add(maquinista_2)
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Maquinista repetido no se ha añadido")
        maquinistas = Maquinista.query.filter_by(nombre_m="Maquinista1").all()
        assert len(maquinistas) == 1, "Se ha añadido más de un maquinista con el mismo nombre"
        print('Exito en operaciones negativas con los maquinsitas')
    except AssertionError as error:
        print('Fallo en el Test operaciones negativas con los maquinistas')
        print(error)

def test_operations_turno():
    print('Operaciones con los turnos')
    try:
        turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_prueba)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        assert turno is not None, "Turno no se ha añadido corerctamente"
        assert turno.nombre_t == "Turno1", "Información del turno no es correcta"
        assert turno.maquina == "Maquina1", "Información del turno no es correcta"
        db.session.delete(turno)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        assert turno is None,"No se ha eliminado el turno corectamente"
        print('Exito en operaciones con los turnos')
    except AssertionError as error:
        print('Fallo en el Test operaciones con los turnos')
        print(error)

def test_operaciones_negativas_turno():
    print('Operaciones negativas con los turnos')
    try:
        turno_1 = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_1)
        turno_2 = Turno(nombre_t="Turno1",maquina="Maquina1")
        try:
            db.session.add(turno_2)
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Turno repetido no se ha añadido")
        turnos = Turno.query.filter_by(nombre_t="Turno1").all()
        assert len(turnos) == 1,"Se ha añadido más de un turno con el mismo nombre"
        print('Exito en operaciones negativas con los turnos')
    except AssertionError as error:
        print('Fallo en el Test operaciones negativas con los turnos')


def test_operations_asign_unasign():
    print('Operaciones asignar y desasignar')
    try:
        maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
        turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_prueba)
        db.session.add(maquinsta_prueba)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        tunro = Turno.query.filter_by(nombre_t="Turno1").first()
        maquinista.turnos.append(turno)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        #append
        assert len(maquinista.turnos) > 0 , "Turno no se ha asignado correctamente"
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        cont = 0
        for turn in maquinista.turnos:
            if turn.nombre_t == "Turno1":
                maquinista.turnos.pop(cont)
            cont += 1
        assert len(maquinista.turnos) == 0 , "Turno no se ha desasignado correctamente"
        print('Existo en operaciones asignar y desasignar')
    except AssertionError as error:
        print('Fallo en el Test de operaciones asignar y desasignar')
