from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador
from . import BaseTestClass
import unittest
class PruebasBBDD(BaseTestClass):
    def test_operations_maquinista(self):
        with self.app.app_context():
            maquinsta_prueba = Maquinista(nombre_m="MaquinistaUNO")
            db.session.add(maquinsta_prueba)
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaUNO").first()
            self.assertEqual(maquinista.nombre_m,"MaquinistaUNO")
            db.session.delete(maquinista)
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaUNO").first()
            self.assertEqual(maquinista,None)
            db.session.commit()

    def test_operations_turno(self):
        with self.app.app_context():
            turno_prueba = Turno(nombre_t="TurnoDOS",maquina="Maquina1")
            db.session.add(turno_prueba)
            turno = Turno.query.filter_by(nombre_t="TurnoDOS",maquina="Maquina1").first()
            self.assertNotEqual(turno, None)
            self.assertEqual(turno.maquina,"Maquina1")
            self.assertEqual(turno.nombre_t,"TurnoDOS")
            db.session.delete(turno)
            turno = Turno.query.filter_by(nombre_t="TurnoDOS",maquina="Maquina1").first()
            self.assertEqual(turno, None)
            db.session.delete(turno)
            db.session.commit()


    def test_operations_asign_unasign(self):
        with self.app.app_context():
            maquinsta_prueba = Maquinista(nombre_m="MaquinistaTRES")
            turno_prueba = Turno(nombre_t="TurnoTRES",maquina="Maquina1")
            db.session.add(turno_prueba)
            db.session.add(maquinsta_prueba)
            db.session.commit()
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRES").first()
            turno = Turno.query.filter_by(nombre_t="TurnoTRES").first()
            maquinista.turnos.append(turno)
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRES").first()
            #append
            self.assertGreater(len(maquinista.turnos),0)
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRES").first()
            cont = 0
            for turn in maquinista.turnos:
                if turn.nombre_t == "TurnoTRES":
                    maquinista.turnos.pop(cont)
                cont += 1
            self.assertEqual(len(maquinista.turnos),0)
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRES").first()
            turno = Turno.query.filter_by(nombre_t="TurnoTRES",maquina="Maquina1").first()
            db.session.delete(maquinista)
            db.session.delete(turno)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
