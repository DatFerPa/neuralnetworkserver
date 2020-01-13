from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hasfallen/', methods=['GET'])
def has_fallen():
    return 'callo' 
if __name__ == '__main__':
    app.run()
