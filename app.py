from flask import Flask
from flask import request
import numpy as np
import tensorflow as tf

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hasfallen/', methods=['GET', 'POST'])
def has_fallen():
    accel = request.args.get('accel')
    corte_1 = accel.split(":")
    lista_accel = []
    for x in corte_1:
        lista = list(map(float,x.split(";")))
        lista_accel.append(lista)

    numpy_lista =
    modelo = tf.keras.models.load_model('modelo_caidas')

    
    return 'caida_si'



if __name__ == '__main__':
    app.run()
