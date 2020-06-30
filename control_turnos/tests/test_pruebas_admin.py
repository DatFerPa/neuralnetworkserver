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
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'se ha añadido',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista.nombre_m,"Maquinista1")
            db.session.delete(maquinista)
            db.session.commit()
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')

    def test_add_maquinista_repetido(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'ya se encuentra',res.data)
        self.client.get('/logoutAdmin/')
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            db.session.delete(maquinista)
            db.session.commit()


    def test_add_turno(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="Turno1",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="Turno2",nombreMaquina="Maquina1"),follow_redirects=True)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
            turno2 = Turno.query.filter_by(nombre_t="Turno2",maquina="Maquina1").first()
            self.assertEqual(turno.nombre_t,"Turno1")
            self.assertEqual(turno.maquina,"Maquina1")
            self.assertEqual(turno.nombre_t,"Turno2")
            self.assertEqual(turno.maquina,"Maquina1")
            db.session.delete(turno)
            db.session.delete(turno2)
            db.session.commit()
            turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
            turno2 = Turno.query.filter_by(nombre_t="Turno2",maquina="Maquina1").first()
            self.assertEqual(turno,None)

        self.client.get('/logoutAdmin/')


    def test_add_turno_repetido(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="Turno1",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'se ha',res.data)
        res = self.client.post('/nuevoTurno/',data=dict(nombreTurno="Turno1",nombreMaquina="Maquina1"),follow_redirects=True)
        self.assertIn(b'ya se encuentra',res.data)
        self.client.get('/logoutAdmin/')
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="Turno1",maquina="Maquina1").first()
            db.session.delete(turno)
            db.session.commit()

        self.client.get('/logoutAdmin/')


    def test_quit_maquinista(self):
        with self.app.app_context():
            maquinista = Maquinista(nombre_m="Maquinista1")
            db.session.add(maquinsta_prueba)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'se ha eliminado',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')

    def test_quit_maquinista_noExiste(self):
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'no se encuentra',res.data)
        with self.app.app_context():
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')



    def test_quit_turno(self):
        with self.app.app_context():
            turno = Turno(nombre_t="Turno1",maquina="Maquina1")
            db.session.add(turno_prueba)
            db.session.commit()
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarTurno/',data=dict(nombreTurno="Turno1"),follow_redirects=True)
        self.assertIn(b'se ha eliminado',res.data)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="Turno1").first()
            self.assertEqual(turno,None)
        self.client.get('/logoutAdmin/')

    def test_quit_turno_noExiste(self):
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="Turno1").first()
            self.assertEqual(turno,None)
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/quitarTurno/',data=dict(nombreTurno="Turno1"),follow_redirects=True)
        self.assertIn(b'no se encuentra',res.data)
        with self.app.app_context():
            turno = Turno.query.filter_by(nombre_t="Turno1").first()
            self.assertEqual(turno,None)
        self.client.get('/logoutAdmin/')














if __name__ == '__main__':
    unittest.main()
