from flask import Blueprint, render_template, request, redirect, url_for
import numpy as np
import tensorflow as tf
from .extensions import db
from .models import Maquinista, Turno, turnos
import os, fnmatch
import azure.storage.common
from azure.storage.common import CloudStorageAccount

main = Blueprint('main',__name__)

@main.route('/')
def principal():
    print("Principal")
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


@main.route('/addTurnos/')
def addTurnos():
    print('addTurnos')
    context = {
        'error_turno':False,
        'ok_turno':False
    }
    if request.args.get('error_turno') is not None:
        context['error_turno'] = True

    if request.args.get('ok_turno') is not None:
        context['ok_turno'] = True

    print(context)
    return render_template('addTurnos.html',**context)

@main.route('/quitTurnos/')
def quitTurnos():
    print('quitTurnos')
    context = {
        'error_turno':False,
        'ok_turno':False
    }
    if request.args.get('error_turno') is not None:
        context['error_turno'] = True

    if request.args.get('ok_turno') is not None:
        context['ok_turno'] = True

    print(context)
    return render_template('quitTurno.html',**context)



@main.route('/addMaquinistas/')
def addMaquinistas():
    print('addMaquinistas')
    context = {
        'error_maquinista':False,
        'ok_maquinista':False
    }
    if request.args.get('error_maquinista') is not None:
        context['error_maquinista'] = True

    if request.args.get('ok_maquinista') is not None:
        context['ok_maquinista'] = True

    print(context)
    return render_template('addMaquinista.html',**context)

@main.route('/quitMaquinistas/')
def quitMaquinistas():
    print('quitMaquinistas')
    context = {
        'error_maquinista':False,
        'ok_maquinista':False
    }
    if request.args.get('error_maquinista') is not None:
        context['error_maquinista'] = True

    if request.args.get('ok_maquinista') is not None:
        context['ok_maquinista'] = True

    print(context)
    return render_template('quitMaquinista.html',**context)

@main.route('/nuevoMaquinista/',methods=['POST'])
def nuevoMaquinista():
    print('nuevoMaquinista')
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        maquinista = Maquinista(nombre_m=nombre)
        db.session.add(maquinista)
        db.session.commit()
        return redirect(url_for('main.addMaquinistas',ok_maquinista=True))
    else:
        return redirect(url_for('main.addMaquinistas',error_maquinista=True))

@main.route('/quitarMaquinista/',methods=['POST'])
def quitarMaquinista():
    print('quitarMaquinista')
    nombre = request.form.get('nombre')
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return redirect(url_for('main.quitMaquinista',error_maquinista=True))
    else:
        db.session.delete(maquinista)
        return redirect(url_for('main.quitMaquinista',ok_maquinista=True))


@main.route('/nuevoTurno/',methods=['POST'])
def nuevoTurno():
    print('nuevoTurno')
    nombreTurno = request.form.get('nombreTurno')
    nombreMaquina = request.form.get('nombreMaquina')
    print(nombreTurno)
    print(nombreMaquina)
    turno = Turno.query.filter_by(nombre_t=nombreTurno,maquina=nombreMaquina).first()
    if turno is None:
        turno = Turno(nomre_t=nombreTurno,maquina=nombreMaquina)
        db.session.add(turno)
        db.session.commit()
        return redirect(url_for('main.addTurnos',ok_turno=True))
    else:
        return redirect(url_for('main.addTurnos',error_turno=True))


@main.route('/quitarTurno/',methods=['POST'])
def quitarTurno():
    print('quitarTurno')
    nombreTurno = request.form.get('nombreTurno')
    turno = Turno.query.filter_by(nombre_t=nombreTurno).first()
    if turno is None:
        return redirect(url_for('main.quitTurnos',error_turno=True))
    else:
        db.session.delete(maquinista)
        return redirect(url_for('main.quitTurnos',ok_turno=True))



@main.route('/buscarTurnosMaquinista/')
def buscarTurnosMaquinista():
    context = {
        'error_maquinista':False,
    }
    if request.args.get('error_maquinista') is not None:
        context['error_maquinista'] = True
    return render_template('buscarMaquinista.html',**context)


@main.route('/listTurnos/',methods=['POST'])
def listTurnos():
    print("listTurnos")
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return redirect(url_for('main.buscarTurnosMaquinsita',error_maquinista=True))

    turnos = []
    for turn in maquinista.turnos:
        turno_actual = Turno.query.filter_by(id=turn.id).first()
        turnos.append(turno_actual)

    context = {
        'turnos':turnos,
        'maquinista':maquinista
    }

    return render_template('listTurnos.html',**context)

@main.route('/gestionTurnos/')
def gestionTurnos():
    print('gestionTurnos')
    maquinistas = Maquinista.query.order_by(Maquinista.nombre_m).all()
    turnos = Turno.query.order_by(Turno.nombre_t).all()
    context = {
        'error_gestion':False,
        'ok_gestion':False,
        'maquinistas':maquinistas,
        'turnos':turnos
    }
    if request.args.get('error_gestion') is not None:
        context['error_gestion'] = True
    if request.args.get('ok_gestion')is not None:
        context['ok_gestion'] = True
    return render_template('gestionTurnos.html',**context)

@main.route('/asignarDenegarTurnos/',methods=['POST'])
def asignarDenegarTurnos():
    context = {
        'error_gestion':False,
        'ok_gestion':False
    }
    nombreMaquinista = request.args.get('nombreMaquinista')
    nombreTurno = request.args.get('nombreTurno')
    gestion = request.args.get('botonGestion')
    print(nombreMaquinista)
    print(nombreTurno)
    print(gestion)
    maquinista = Maquinista.query.filter_by(nombre_m=nombreMaquinista).first()
    turno = Turno.query.filter_by(nombre_t=nombreTurno).first()
    if maquinista is None and turno is None:
        return redirect(url_for('main.gestionTurnos',error_gestion=True))

    if gestion == "Asignar":
        #comprobar si el turno ya esta asignado
        for turn in maquinista.turnos:
            if turn.nombre_t == turno.nombre_t:
                context['error_gestion']:True
                return render_template('gestionTurnos.html',**context)
        maquinista.turnos.append(turno)
        db.session.commit()
        return redirect(url_for('main.gestionTurnos',ok_gestion=True))

    elif gestion == "Denegar":
        cont = 0
        for turn in maquinista.turnos:
            if turn.nombre_t == turno.nombre_t:
                maquinista.turnos.pop(cont)
                return redirect(url_for('main.gestionTurnos',ok_gestion=True))

            cont += 1
    else:
        return redirect(url_for('main.gestionTurnos',error_gestion=True))

@main.route('/ficherosTurno/')
def ficherosTurno():
    print("ficherosTurno")
    maquinistaID = request.args.get('maquinista_arg')
    turno_actID = request.args.get('turno_arg')
    maquinista = Maquinista.query.filter_by(id=maquinistaID).first()
    turno_act = Turno.query.filter_by(id=turno_actID).first()
    print(maquinista.nombre_m)
    print(turno_act.nombre_t)


    pattern = maquinista.nombre_m+" "+turno_act.nombre_t
    ficheros_logs = []
    fechas_ficheros = []

    STORAGE_ACCOUNT_NAME = 'ficherosmaquinistas'
    STORAGE_ACCOUNT_KEY  = 'JKGDYu80C4HWg6DxUyA8mWYouPVAHV9tlB8MO6Xcv5sFKR7KVr+Onw7PLwP7KjMqhdPKTCWFk59NM4m+t/lcGQ=='

    account = CloudStorageAccount(STORAGE_ACCOUNT_NAME,STORAGE_ACCOUNT_KEY)

    file_service = account.create_file_service()

    files = list(file_service.list_directories_and_files('shareficherosmaquinistas',prefix=pattern))
    print("busqueda de ficheros")
    for file in files:
        print(file.name)
        textos = file.name.split(',')
        print(textos)
        ficheros_logs.append(file.name)
        valores = textos[1].split('.txt')
        print(valores)
        fechas_ficheros.append(valores[0])
        print("---------")

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

    STORAGE_ACCOUNT_NAME = 'ficherosmaquinistas'
    STORAGE_ACCOUNT_KEY  = 'JKGDYu80C4HWg6DxUyA8mWYouPVAHV9tlB8MO6Xcv5sFKR7KVr+Onw7PLwP7KjMqhdPKTCWFk59NM4m+t/lcGQ=='

    account = CloudStorageAccount(STORAGE_ACCOUNT_NAME,STORAGE_ACCOUNT_KEY)

    file_service = account.create_file_service()
    file_and_contenido =file_service.get_file_to_text('shareficherosmaquinistas',None,nombre)

    filas = file_and_contenido.content.split('\n')
    print(filas)

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

        lista_split = contenido.split(";")
        texto ="";
        for i in lista_split:
            texto = texto+ i + "\n"


        STORAGE_ACCOUNT_NAME = 'ficherosmaquinistas'
        STORAGE_ACCOUNT_KEY  = 'JKGDYu80C4HWg6DxUyA8mWYouPVAHV9tlB8MO6Xcv5sFKR7KVr+Onw7PLwP7KjMqhdPKTCWFk59NM4m+t/lcGQ=='

        account = CloudStorageAccount(STORAGE_ACCOUNT_NAME,STORAGE_ACCOUNT_KEY)
        file_service = account.create_file_service()

        file_service.create_file_from_text(
        "shareficherosmaquinistas",
        None,
        nombreMaquinista+" "+nombreTurno+", Fecha "+fecha+" Hora "+hora+".txt",
        texto)

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
