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
            db.session.command()
            maquinista = Maquinista.query.filter_by(nombre_m="Maquinista1").first()
            self.assertEqual(maquinista,None)
        self.client.get('/logoutAdmin/')

    def test_add_maquinista_repetido(self):
        self.client.post('/loginAdmin/',data=dict(nombreAdmin="admin",passwordAdmin="admin"),follow_redirects=True)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'se ha añadido',res.data)
        res = self.client.post('/nuevoMaquinista/',data=dict(nombre="Maquinista1"),follow_redirects=True)
        self.assertIn(b'ya se encuentra',res.data)
        self.client.get('/logoutAdmin/')





if __name__ == '__main__':
    unittest.main()
