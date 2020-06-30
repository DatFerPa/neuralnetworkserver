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
        self.assertIn(b'Iniciar sesion de administrador',res.data)















if __name__ == '__main__':
    unittest.main()
