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
