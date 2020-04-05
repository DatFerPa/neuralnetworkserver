from .extensions import db

turnos = db.Table('turnos',
db.Column('maquinista_id',db.Integer,db.ForeignKey('maquinista.id'),primary_key=True),
db.Column('turno_id',db.Integer,db.ForeignKey('turno.id'),primary_key=True)
)

class Maquinista(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre_m = db.Column(db.String(80), unique=True, nullable=False)
    turnos = db.relationship('Turno',secondary=turnos,lazy='subquery',
        backref=db.backref('maquinistas',lazy=True))

class Turno(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre_t = db.Column(db.String(50),unique=True,nullable=False)
    maquina = db.Column(db.String(50),unique=True,nullable=False)
