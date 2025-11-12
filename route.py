from bottle import Bottle, run, static_file

app = Bottle()

# Página inicial (login e cadastro)
@app.route('/')
def index():
    return static_file('index.html', root='./views')

# Página principal (home)
@app.route('/home')
def home():
    return static_file('home.html', root='./views')

# Servir arquivos estáticos (CSS, JS, imagens, etc)
@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./views')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
