from bottle import Bottle, run, template, static_file
import os

app = Bottle()

# Caminho absoluto da pasta views
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

@app.route('/')
def home():
    return template('index', template_lookup=[VIEWS_DIR])

# Rota para arquivos estáticos (CSS, JS, imagens, etc)
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=VIEWS_DIR)

# Inicia o servidor
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
