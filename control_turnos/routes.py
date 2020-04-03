from flask import BLueprints, render_template

from .extensions import db
from .models import User, Turno

main = BLueprint('main',__name)

@main.route('/')
def principal():
    return render_template('principal.html')
