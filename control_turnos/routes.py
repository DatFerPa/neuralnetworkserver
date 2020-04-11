from flask import Blueprint, render_template, request

from .extensions import db
from .models import Maquinista, Turno, turnos

main = Blueprint('main',__name__)

@main.route('/')
def principal():
    return render_template('principal.html')

@main.route('/login/',methods=['POST'])
def login():
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    print(maquinista)
    if maquinista is None:
        return 'no'
    else:
        return 'si'

@main.route('/turnos/',methods=['POST'])
def turnos():
    nombre = request.form.get('nombre')
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    print(maquinista)
    turnos_de_un_maquinista = []
    print(maquinista.turnos)
    for turn in maquinista.turnos:
        turno_actual = Turno.query.filter_by(id=turn.id).first()
        turnos_de_un_maquinista.append(turno_actual)

    concatenacion_turnos=""
    iteracion = len(turnos_de_un_maquinista)

    for n in range(iteracion):
        concatenacion_turnos = concatenacion_turnos + turnos_de_un_maquinista[n].nombre_t + ";" + turnos_de_un_maquinista[n].maquina
        if n != (iteracion-1):
            concatenacion_turnos = concatenacion_turnos + ":"

    return concatenacion_turnos
