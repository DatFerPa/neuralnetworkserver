from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador
from . import BaseTestClass
import unittest
class PruebasBBDD(BaseTestClass):
    def test_operations_maquinista(self):
        with self.app.app_context():
            maquinsta_prueba = Maquinista(nombre_m="Maquinista1")
            db.session.add(maquinsta_prueba)
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista.nombre_m,"Maquinista1")
            db.session.delete(maquinista)
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)


    def test_operations_turno(self):
        with self.app.app_context():
            turno_prueba = Turno(nombre_t="Turno1",maquina="Maquina1")
            db.session.add(turno_prueba)
            turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
            self.assertNotEqual(turno, None)
            self.assertEqual(turno.maquina,"Maquina1")
            self.assertEqual(turno.nombre_t,"Turno1")
            db.session.delete(turno)
            turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
            self.assertEqual(turno, None)


    def test_operations_asign_unasign(self):
        with self.app.app_context():
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


if __name__ == '__main__':
    unittest.main()
