from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
import numpy as np
import tensorflow as tf
from control_turnos.extensions import db
from control_turnos.models import Maquinista, Turno, turnos, Administrador
import os, fnmatch
import azure.storage.common
from azure.storage.common import CloudStorageAccount

androidRoutes = Blueprint('androidRoutes',__name__)


import pusher

pusher_client = pusher.Pusher(
  app_id='1014550',
  key='33da5fe2d909596436d5',
  secret='015d1e8981ad3a6a0e3b',
  cluster='eu',
  ssl=True
)


@androidRoutes.route('/login/',methods=['POST'])
def login():
    nombre = request.form.get('nombre')
    print(nombre)
    maquinista = Maquinista.query.filter_by(nombre_m=nombre).first()
    print(maquinista)
    if maquinista is None:
        return 'no'
    else:
        return 'si'


@androidRoutes.route('/turnos/',methods=['POST'])
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



@androidRoutes.route('/addLogTurno/',methods=['POST'])
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



@androidRoutes.route('/pushNotificacion/',methods=['POST'])
def pushNotificacion():

    nombreFichero = request.form.get('nombreFichero')
    nombreFicheroSplit = nombreFichero.split(',')
    nombre_y_turno = nombreFicheroSplit[0].split(',')
    nombre = nombre_y_turno[0]
    turno = nombre_y_turno[1] + " "
    fecha = nombreFicheroSplit[1]
    emergencia = nombreFicheroSplit[2].replace('.txt','')
    pusher_client.trigger('my-channel', 'my-event', {'maquinista': nombre,'turno':turno,'fecha':fecha,'nombreFichero':nombreFichero})

    return 'Notificacion realizada'
