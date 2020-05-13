from flask import Blueprint, render_template, request, redirect, url_for
import numpy as np
import tensorflow as tf
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
    pattern = maquinista.nombre_m+" "+turno_act.nombre_t+"*"
    print(pattern)
    ficheros_logs = []
    fechas_ficheros = []
    for entry in listFicheros:
        print(entry)
        try:
            if fnmatch.fnmatch(entry, pattern):
                    print (entry)
                    ficheros_logs.append(entry)
                    valores = entry.split(",")
                    fechas_ficheros.append(valores[1])
        except FileNotFoundError:
            print("Fichero no existe")
        except:
            print("Otro problema")

    context = {
        'ficheros_logs':ficheros_logs,
        'fechas_ficheros':fechas_ficheros,
        'nombre_turno':turno_act.nombre_t
    }

    return render_template('ficherosTurno.html',**context)

@main.route('/logsTurno/')
def logsTurno():
    print("logsTurno")
    nombre = request.args.get('nombre_fichero_arg')
    path_fichero = os.path.abspath(os.getcwd())+"/control_turnos/logturnos/"+nombre
    filas = []

    file = open(path_fichero,"r")
    for fila in file:
        filas.append(fila)

    context = {
        'fecha':request.args.get('fecha_fichero_arg'),
        'nombre_turno':request.args.get('nombre_turno_arg'),
        'filas':filas
    }

    return render_template('logsTurno.html',**context)



@main.route('/addLogTurno/',methods=['POST'])
def addLogTurno():
    print("addLogTurno")
    try:
        nombreMaquinista = request.form.get('nombreMaquinista')
        nombreTurno = request.form.get('nombreTurno')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        contenido = request.form.get('contenido')
        path_fichero = os.path.abspath(os.getcwd())+"/control_turnos/logturnos/"

        f = open(path_fichero+nombreMaquinista+" "+nombreTurno+", Fecha "+fecha+" Hora "+hora+".txt","w+")
        lista_split = contenido.split(";")

        for i in lista_split:
            f.write(i  + "\n")

        f.close()

    except:
        return "turnoFalseAdd"

    return "turnoTrueAdd"


@main.route('/getIsOk/',methods=['POST'])
def getIsOk():
    print("getIsOk")
    accel = request.form.get('accel')
    corte_1 = accel.split(":")
    lista_accel = []
    for x in corte_1:
        lista = list(map(float,x.split(";")))
        lista_accel.append(lista)
    lista_previa = []
    lista_previa.append(lista_accel)
    print(lista_previa)
    numpy_lista = np.array(lista_previa)
    modelo = tf.keras.models.load_model('modelo_movimientos')
    prediccion = modelo.predict(numpy_lista)
    prediccion_max = np.argmax(prediccion[0])
    print("Si movimiento: "+prediccion[0][0]+" -  No movimiento: "+prediccion[0][1])
    print("Prediccion maxima para: "+prediccion_max)
    #si movimiento 0 no movimiento 1
    if prediccion_max == 0:
        return "siMovimiento"

    return "noMovimiento"
