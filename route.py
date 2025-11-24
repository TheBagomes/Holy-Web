from bottle import Bottle, run, static_file, request, redirect
from models.user import User
from models.database import get_db   # ou database import get_db

app = Bottle()

@app.route('/')
def index():
    return static_file('index.html', root='./views')

@app.post('/register')
def register():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    db = get_db()
    user = User(nome, email, senha)
    user.save(db)

    return redirect('/home')

@app.post('/login')
def login():
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    db = get_db()
    user = User.get_by_email(db, email)

    if user and user.senha == senha:
        return redirect('/home')
    else:
        return "Login inválido!"

@app.route('/home')
def home():
    return static_file('home.html', root='./views')

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./views')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
