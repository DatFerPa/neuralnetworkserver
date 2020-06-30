from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador
from . import BaseTestClass
import unittest
class PruebasAdmin(BaseTestClass):

    def test_haciendo_login(self):
        res = self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        self.assertIn(b'Panel de control',res.data)
        self.client.get('/logoutAdmin/')

    def test_entrando_sin_login(self):
        res = self.client.get('/addTurnos/')
        self.assertIn(b'Redirecting',res.data)

    def test_add_maquinista(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="MaquinistaCUATRO"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaCUATRO").first()
            self.assertEqual(maquinista.nombre_m,"MaquinistaCUATRO")
            db.session.delete(maquinista)
            db.session.commit()
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaCUATRO").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')

    def test_add_maquinista_repetido(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="MaquinistaCINCO"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="MaquinistaCINCO"),follow_redirects=True)
        self.assertIn(b'ya se encuentra',res.data)
        self.client.get('/logoutAdmin/')
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaCINCO").first()
            db.session.delete(maquinista)
            db.session.commit()


    def test_add_turno(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="TurnoSEIS",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="TurnoSIETE",nombreMaquina="Maquina1"),follow_redirects=True)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="TurnoSEIS",maquina="Maquina1").first()
            turno2 = Turno.query.filter_by(nombre_t="TurnoSIETE",maquina="Maquina1").first()
            self.assertEqual(turno.nombre_t,"TurnoSEIS")
            self.assertEqual(turno.maquina,"Maquina1")
            self.assertEqual(turno2.nombre_t,"TurnoSIETE")
            self.assertEqual(turno2.maquina,"Maquina1")
            db.session.delete(turno)
            db.session.delete(turno2)
            db.session.commit()
            turno = Turno.query.filter_by(nombre_t="TurnoSEIS",maquina="Maquina1").first()
            turno2 = Turno.query.filter_by(nombre_t="TurnoSIETE",maquina="Maquina1").first()
            self.assertEqual(turno,None)
            self.assertEqual(turno2,None)

        self.client.get('/logoutAdmin/')


    def test_add_turno_repetido(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="TurnoOCHO",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="TurnoOCHO",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'ya se encuentra',res.data)
        self.client.get('/logoutAdmin/')
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="TurnoOCHO",maquina="Maquina1").first()
            db.session.delete(turno)
            db.session.commit()

        self.client.get('/logoutAdmin/')


    def test_quit_maquinista(self):
        with self.app.app_context():
            maquinista = Maquinista(nombre_m="MaquinistaNUEVE")
            db.session.add(maquinista)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarMaquinista/',data=dict(nombre="MaquinistaNUEVE"),follow_redirects=True)
        self.assertIn(b'se ha eliminado',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaNUEVE").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')

    def test_quit_maquinista_noExiste(self):
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaDIEZ").first()
            self.assertEqual(maquinista,None)
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarMaquinista/',data=dict(nombre="MaquinistaDIEZ"),follow_redirects=True)
        self.assertIn(b'no se encuentra',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaDIEZ").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')



    def test_quit_turno(self):
        with self.app.app_context():
            turno = Turno(nombre_t="TurnoONCE",maquina="Maquina1")
            db.session.add(turno)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarTurno/',data=dict(nombreTurno="TurnoONCE"),follow_redirects=True)
        self.assertIn(b'se ha eliminado',res.data)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="TurnoONCE").first()
            self.assertEqual(turno,None)
        self.client.get('/logoutAdmin/')

    def test_quit_turno_noExiste(self):
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="TurnoDOCE").first()
            self.assertEqual(turno,None)
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarTurno/',data=dict(nombreTurno="TurnoDOCE"),follow_redirects=True)
        self.assertIn(b'no se encuentra',res.data)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="TurnoDOCE").first()
            self.assertEqual(turno,None)
        self.client.get('/logoutAdmin/')

    def test_enlazar_desenlazar(self):
        with self.app.app_context():
            maquinista = Maquinista(nombre_m="MaquinistaTRECE")
            turno = Turno(nombre_t="TurnoTRECE",maquina="Maquina1")
            db.session.add(maquinista)
            db.session.add(turno)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/asignarDesasignarTurnos/',data=dict(nombreMaquinista="MaquinistaTRECE",nombreTurno="TurnoTRECE",botonGestion="Asignar"),follow_redirects=True)
        self.assertIn(b'Se ha podido realizar la',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRECE").first()
            self.assertEqual(len(maquinista.turnos),1)
            turno = Turno.query.filter_by(nombre_t="TurnoTRECE").first()
            self.assertEqual(len(turno.maquinistas),1)
        res = self.client.post('/asignarDesasignarTurnos/',data=dict(nombreMaquinista="MaquinistaTRECE",nombreTurno="TurnoTRECE",botonGestion="Desasignar"),follow_redirects=True)
        self.assertIn(b'Se ha podido realizar la',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaTRECE").first()
            self.assertEqual(len(maquinista.turnos),0)
            turno = Turno.query.filter_by(nombre_t="TurnoTRECE").first()
            self.assertEqual(len(turno.maquinistas),0)
            db.session.delete(maquinista)
            db.session.delete(turno)
            db.session.commit()
        self.client.get('/logoutAdmin/')

    def test_enlazar_desenlazar_mal(self):
        with self.app.app_context():
            maquinista = Maquinista(nombre_m="MaquinistaCATORCE")
            turno = Turno(nombre_t="TurnoCATORCE",maquina="Maquina1")
            db.session.add(maquinista)
            db.session.add(turno)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/asignarDesasignarTurnos/',data=dict(nombreMaquinista="MaquinistaCATORCE",nombreTurno="TurnoCATORCE",botonGestion="Desasignar"),follow_redirects=True)
        self.assertIn(b'Revise si los datos son correctos',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaCATORCE").first()
            self.assertEqual(len(maquinista.turnos),0)
            turno = Turno.query.filter_by(nombre_t="TurnoCATORCE").first()
            self.assertEqual(len(turno.maquinistas),0)
            maquinista.turnos.append(turno)
            db.session.commit()
        res = self.client.post('/asignarDesasignarTurnos/',data=dict(nombreMaquinista="MaquinistaCATORCE",nombreTurno="TurnoCATORCE",botonGestion="Asignar"),follow_redirects=True)
        self.assertIn(b'Revise si los datos son correctos',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="MaquinistaCATORCE").first()
            self.assertEqual(len(maquinista.turnos),1)
            turno = Turno.query.filter_by(nombre_t="TurnoCATORCE").first()
            self.assertEqual(len(turno.maquinistas),1)
            db.session.delete(maquinista)
            db.session.delete(turno)
            db.session.commit()
        self.client.get('/logoutAdmin/')



if __name__ == '__main__':
    unittest.main()
