from flask import Blueprints, render_template

from .extensions import db
from .models import User, Turno

main = BLueprint('main',__name__)

@main.route('/')
def principal():
    return render_template('principal.html')

@main.route('/login/',methods=['POST'])
def login():
    nombre = request.args.get('nombre')
