from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador
from . import BaseTestClass
import unittest
class PruebasBBDD(BaseTestClass):
    def test_operations_maquinista(self):
        print('Operaciones con los maquinistas')
        maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
        db.session.add(maquinsta_prueba)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        self.assertEqual(maquinista.nombre_m,"Maquinista1")
        db.session.delete(maquinista)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        self.assertEqual(maquinista.nombre_m,None)
        print('Exito en operaciones con los maquinistas')

    def test_operaciones_negativas_maquinista(self):
        print('Operaciones negativas con los maquinsitas')
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
        self.assertEqual(len(maquinistas),1)
        print('Exito en operaciones negativas con los maquinsitas')


    def test_operations_turno(self):
        print('Operaciones con los turnos')
        turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_prueba)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        self.assertEqual(turno,not None)
        self.assertEqual(turno.maquina,"Maquina1")
        self.assertEqual(turno.nombre_t,"Turno1")
        db.session.delete(turno)
        turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
        assert turno is None,"No se ha eliminado el turno corectamente"
        print('Exito en operaciones con los turnos')


    def test_operaciones_negativas_turno(self):
        print('Operaciones negativas con los turnos')
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
        self.assertEqual(len(turnos),1)
        print('Exito en operaciones negativas con los turnos')


    def test_operations_asign_unasign(self):
        print('Operaciones asignar y desasignar')
        maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
        turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
        db.session.add(turno_prueba)
        db.session.add(maquinsta_prueba)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        turno = Turno.query.filter_by(nombre_t="Turno1").first()
        maquinista.turnos.append(turno)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        #append
        self.assertGreater(len(maquinista.turnos),0)
        maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
        cont = 0
        for turn in maquinista.turnos:
            if turn.nombre_t == "Turno1":
                maquinista.turnos.pop(cont)
            cont += 1
        self.assertEqual(len(maquinista.turnos),0)
        print('Existo en operaciones asignar y desasignar')
