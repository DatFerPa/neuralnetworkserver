from .extensions import db
from flask_login import UserMixin

turnos = db.Table('turnos',
db.Column('maquinista_id',db.Integer,db.ForeignKey('maquinista.id'),primary_key=True),
db.Column('turno_id',db.Integer,db.ForeignKey('turno.id'),primary_key=True)
)

class Maquinista(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre_m = db.Column(db.String(80), unique=True, nullable=False)
    turnos = db.relationship('Turno',secondary=turnos,lazy='subquery',
        backref=db.backref('maquinistas',single_parent=True,lazy=True))

class Turno(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre_t = db.Column(db.String(50),unique=True,nullable=False)
    maquina = db.Column(db.String(50),unique=True,nullable=False)

class Administrador(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre_admin = db.Column(db.String(50),unique=True,nullable=False)
    password_admin = db.Column(db.String(50),nullable=False)
