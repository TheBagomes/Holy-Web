from bottle import Bottle, run, static_file, request, redirect, template, response
from models.user import User
from database import criar_tabelas

app = Bottle()

criar_tabelas()

@app.route('/')
def index():
    return static_file('index.html', root='./views')

@app.post('/register')
def register():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    user = User(nome, email, senha)
    user.save()
        
    return redirect('/')


@app.post('/login')
def login():
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    user = User.get_by_email(email)

    if not user:
        return "<h3>Usuário não existe! <a href='/'>Voltar</a></h3>"

    if user[3] != senha:
        return "<h3>Senha incorreta! <a href='/'>Voltar</a></h3>"

    response.set_cookie("usuario_logado", user[2], secret="CHAVE_SECRETA")
    return redirect('/home')

@app.get('/logout')
def logout():
    response.delete_cookie("usuario_logado")
    return redirect('/')

@app.route('/home')
def home():
    usuario = request.get_cookie("usuario_logado", secret="CHAVE_SECRETA")
    if not usuario:
        return redirect("/")
    return static_file('home.html', root='./views')

@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./views')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
