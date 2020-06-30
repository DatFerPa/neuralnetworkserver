from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
import numpy as np
import tensorflow as tf
from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, turnos, Administrador
import os, fnmatch
import azure.storage.common
from azure.storage.common import CloudStorageAccount

webRoutes = Blueprint('webRoutes',__name__)

@webRoutes.route('/')
def principal():
    print("Principal")
    context = {
        'error_login':False
    }
    if request.args.get('error_login') is not None:
        context['error_login'] = True

    return render_template('principal.html',**context)

@webRoutes.route('/loginAdmin/', methods=['POST'])
def loginAdmin():
    nombreAdmin = request.form.get('nombreAdmin')
    passwordAdmin = request.form.get('passwordAdmin')

    admin = Administrador.query.filter_by(nombre_admin=nombreAdmin,password_admin=passwordAdmin).first()

    if not admin:
        return redirect(url_for('webRoutes.principal',error_login=True))
    else:
        login_user(admin)
        return redirect(url_for('webRoutes.dashboardAdmin'))

@webRoutes.route('/logoutAdmin/')
@login_required
def logoutAdmin():
    logout_user()
    return redirect(url_for('webRoutes.principal'))

@webRoutes.route('/dashboardAdmin/')
@login_required
def dashboardAdmin():
    print('dashboardAdmin')
    return render_template('dashboardAdmin.html')


@webRoutes.route('/addTurnos/')
@login_required
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

@webRoutes.route('/quitTurnos/')
@login_required
def quitTurnos():
    print('quitTurnos')
    turnos = Turno.query.order_by(Turno.nombre_t).all()
    context = {
        'error_turno':False,
        'ok_turno':False,
        'turnos':turnos
    }
    if request.args.get('error_turno') is not None:
        context['error_turno'] = True

    if request.args.get('ok_turno') is not None:
        context['ok_turno'] = True

    print(context)
    return render_template('quitTurno.html',**context)



@webRoutes.route('/addMaquinistas/')
@login_required
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

@webRoutes.route('/quitMaquinistas/')
@login_required
def quitMaquinistas():
    print('quitMaquinistas')
    maquinistas = Maquinista.query.order_by(Maquinista.nombre_m).all()
    context = {
        'error_maquinista':False,
        'ok_maquinista':False,
        'maquinistas':maquinistas
    }
    if request.args.get('error_maquinista') is not None:
        context['error_maquinista'] = True

    if request.args.get('ok_maquinista') is not None:
        context['ok_maquinista'] = True

    print(context)
    return render_template('quitMaquinista.html',**context)

@webRoutes.route('/nuevoMaquinista/',methods=['POST'])
@login_required
def nuevoMaquinista():
    print('nuevoMaquinista')
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        maquinista = Maquinista(nombre_m=nombre)
        db.session.add(maquinista)
        db.session.commit()
        return redirect(url_for('webRoutes.addMaquinistas',ok_maquinista=True))
    else:
        return redirect(url_for('webRoutes.addMaquinistas',error_maquinista=True))

@webRoutes.route('/quitarMaquinista/',methods=['POST'])
@login_required
def quitarMaquinista():
    print('quitarMaquinista')
    nombre = request.form.get('nombre')
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return redirect(url_for('webRoutes.quitMaquinistas',error_maquinista=True))
    else:
        db.session.delete(maquinista)
        db.session.commit()

        STORAGE_ACCOUNT_NAME = 'ficherosmaquinistas'
        STORAGE_ACCOUNT_KEY  = 'JKGDYu80C4HWg6DxUyA8mWYouPVAHV9tlB8MO6Xcv5sFKR7KVr+Onw7PLwP7KjMqhdPKTCWFk59NM4m+t/lcGQ=='
        account = CloudStorageAccount(STORAGE_ACCOUNT_NAME,STORAGE_ACCOUNT_KEY)
        file_service = account.create_file_service()
        files = list(file_service.list_directories_and_files('shareficherosmaquinistas',prefix=maquinista.nombre_m))
        for file in files:
            print(file.name)
            file_service.delete_file(
                "shareficherosmaquinistas",
                None,
                file.name
            )
            print("--------------------")

        return redirect(url_for('webRoutes.quitMaquinistas',ok_maquinista=True))


@webRoutes.route('/nuevoTurno/',methods=['POST'])
@login_required
def nuevoTurno():
    print('nuevoTurno')
    nombreTurno = request.form.get('nombreTurno')
    nombreMaquina = request.form.get('nombreMaquina')
    print(nombreTurno)
    print(nombreMaquina)
    turno = Turno.query.filter_by(nombre_t=nombreTurno,maquina=nombreMaquina).first()
    if turno is None:
        turno = Turno(nombre_t=nombreTurno,maquina=nombreMaquina)
        db.session.add(turno)
        db.session.commit()
        return redirect(url_for('webRoutes.addTurnos',ok_turno=True))
    else:
        return redirect(url_for('webRoutes.addTurnos',error_turno=True))


@webRoutes.route('/quitarTurno/',methods=['POST'])
@login_required
def quitarTurno():
    print('quitarTurno')
    nombreTurno = request.form.get('nombreTurno')
    turno = Turno.query.filter_by(nombre_t=nombreTurno).first()
    print(turno)
    if turno is None:
        return redirect(url_for('webRoutes.quitTurnos',error_turno=True))
    else:
        db.session.delete(turno)
        db.session.commit()
        return redirect(url_for('webRoutes.quitTurnos',ok_turno=True))


@webRoutes.route('/buscarRegistrosMaquinista/')
@login_required
def buscarRegistrosMaquinista():
    maquinistas = Maquinista.query.order_by(Maquinista.nombre_m).all()
    context = {
        'maquinistas':maquinistas,
        'error_maquinista':False
    }
    if request.args.get('error_maquinista') is not None:
        context['error_maquinista'] = True
    return render_template('buscarMaquinista.html',**context)


@webRoutes.route('/listTurnos/',methods=['POST'])
@login_required
def listTurnos():
    print("listTurnos")
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    if maquinista is None:
        return redirect(url_for('webRoutes.buscarRegistrosMaquinista',error_maquinista=True))

    turnos = []
    for turn in maquinista.turnos:
        turno_actual = Turno.query.filter_by(id=turn.id).first()
        turnos.append(turno_actual)

    context = {
        'turnos':turnos,
        'maquinista':maquinista
    }

    return render_template('listTurnos.html',**context)

@webRoutes.route('/gestionTurnos/')
@login_required
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

@webRoutes.route('/asignarDesasignarTurnos/',methods=['POST'])
@login_required
def asignarDesasignarTurnos():
    print("asignarDesasignarTurnos")
    context = {
        'error_gestion':False,
        'ok_gestion':False
    }
    nombreMaquinista = request.form.get('nombreMaquinista')
    nombreTurno = request.form.get('nombreTurno')
    gestion = request.form.get('botonGestion')
    print(nombreMaquinista)
    print(nombreTurno)
    print(gestion)
    maquinista = Maquinista.query.filter_by(nombre_m=nombreMaquinista).first()
    turno = Turno.query.filter_by(nombre_t=nombreTurno).first()
    print(maquinista)
    print(turno)
    if maquinista is None and turno is None:
        return redirect(url_for('webRoutes.gestionTurnos',error_gestion=True))

    if gestion == "Asignar":
        print("Asignar")
        for turn in maquinista.turnos:
            if turn.nombre_t == turno.nombre_t:
                context['error_gestion']:True
                return redirect(url_for('webRoutes.gestionTurnos',error_gestion=True))
        maquinista.turnos.append(turno)
        db.session.commit()
        return redirect(url_for('webRoutes.gestionTurnos',ok_gestion=True))

    elif gestion == "Desasignar":
        print("Desasignar")
        cont = 0
        for turn in maquinista.turnos:
            print(turn.nombre_t)
            if turn.nombre_t == turno.nombre_t:
                maquinista.turnos.pop(cont)
                db.session.commit()
                return redirect(url_for('webRoutes.gestionTurnos',ok_gestion=True))

            cont += 1

        return redirect(url_for('webRoutes.gestionTurnos',error_gestion=True))

    else:
        return redirect(url_for('webRoutes.gestionTurnos',error_gestion=True))

@webRoutes.route('/ficherosTurno/')
@login_required
def ficherosTurno():
    print("ficherosTurno")
    maquinistaID = request.args.get('maquinista_arg')
    turno_actID = request.args.get('turno_arg')
    maquinista = Maquinista.query.filter_by(id=maquinistaID).first()
    turno_act = Turno.query.filter_by(id=turno_actID).first()
    print(maquinista.nombre_m)
    print(turno_act.nombre_t)


    pattern = maquinista.nombre_m+","+turno_act.nombre_t
    print(pattern)
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
        valores = textos[2].split('.txt')
        print(valores)
        fechas_ficheros.append(valores[0])
        print("---------")

    context = {
        'ficheros_logs':ficheros_logs,
        'fechas_ficheros':fechas_ficheros,
        'nombre_turno':turno_act.nombre_t
    }

    return render_template('ficherosTurno.html',**context)

@webRoutes.route('/logsTurno/')
@login_required
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
