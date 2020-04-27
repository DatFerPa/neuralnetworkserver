from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db
from .models import Maquinista, Turno, turnos
import os, fnmatch
main = Blueprint('main',__name__)

@main.route('/')
def principal():
    print("Principal")
    context = {
        'error_maquinista':False
    }
    if request.args.get('error_maquinista') is not None:
        context = {
            'error_maquinista':True
        }

    print(context)
    return render_template('principal.html',**context)

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

@main.route('/listTurnos/',methods=['POST'])
def listTurnos():
    print("listTurnos")
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return redirect(url_for('main.principal',error_maquinista=True))

    turnos = []
    for turn in maquinista.turnos:
        turno_actual = Turno.query.filter_by(id=turn.id).first()
        turnos.append(turno_actual)

    context = {
        'turnos':turnos,
        'maquinista':maquinista
    }

    return render_template('listTurnos.html',**context)

#llegarr a este a traes de un url_for, y meter parametros en la funcion
@main.route('/ficherosTurno/')
def ficherosTurno():
    print("ficherosTurno")
    maquinistaID = request.args.get('maquinista_arg')
    turno_actID = request.args.get('turno_arg')
    maquinista = Maquinista.query.filter_by(id=maquinistaID).first()
    turno_act = Turno.query.filter_by(id=turno_actID).first()
    print(maquinista.nombre_m)
    print(turno_act.nombre_t)

    listFicheros = os.listdir(os.path.abspath(os.getcwd())+"/control_turnos/logturnos")
    print(listFicheros)


"""
    pattern = maquinista.nombre_m+turno_act.nombre_t+"*"
    for entry in list:
        if fnmatch.fnmatch(entry, pattern):
                print (entry)
"""
    context = {
        'valor':1
    }


    return render_template('ficherosTurno.html',**context)

@main.route('/logsTurno/')
def logsTurno():
    print("logsTurno")

    context = {

    }

    return render_template('logsTurno.html')

@main.route('/addLogTurno/',methods=['POST'])
def addLogTurno():

    return "si"
