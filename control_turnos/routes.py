from flask import Blueprint, render_template

from .extensions import db
from .models import Maquinista, Turno

main = Blueprint('main',__name__)

@main.route('/')
def principal():
    return render_template('principal.html')

@main.route('/login/',methods=['POST'])
def login():
    nombre = request.args.get('nombre')
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return 'no'
    else:
        return 'si'

@main.route('/turnos/',methods=['POST'])
def login():
    nombre = request.args.get('nombre')
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    turnos_union = turnos.query.filter_by(maquinista_id=maquinista.id).all()
    turnos_de_un_maquinista = []

    for turn in turnos_union:
        turno_actual = Turno.query.filter_by(id=turn.turno_id).first()
        turnos_de_un_maquinista.append(turno_actual)

    concatenacion_turnos=""
    iteracion = len(turnos_de_un_maquinista) - 1

    for n in range(iteracion):
        concatenacion_turnos = concatenacion_turnos + turnos_de_un_maquinista[n].nombre_t + ";" + turnos_de_un_maquinista[n].maquina
        if n != iteracion:
            concatenacion_turnos = concatenacion_turnos + ":"

    return concatenacion_turnos
