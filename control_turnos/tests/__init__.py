import unittest
from control_turnos import create_app
from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, Administrador


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_file="settings_testing.py")
        self.client = self.app.test_client()
