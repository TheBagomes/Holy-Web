from bottle import Bottle, template, static_file

app = Bottle()

@app.route('/')
def home():
    return template('index')

@app.route('/static/<filename:path>')
def static_files(filename):
    return static_file(filename, root='./app/views/static')
