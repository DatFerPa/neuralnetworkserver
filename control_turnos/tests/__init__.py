import unittest
from control_turnos import create_app
from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_file="settings_testing.py")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
