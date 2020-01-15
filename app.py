from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hasfallen/', methods=['GET', 'POST'])
def has_fallen():
    accel = request.args.get('accel')
    print(accel)
    return 'callo'



if __name__ == '__main__':
    app.run()
