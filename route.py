from bottle import Bottle, run, static_file, request, redirect, template, response
from models.user import User
from database import criar_tabelas

app = Bottle()

criar_tabelas()

# ------------------------------------------
# INDEX
# ------------------------------------------
@app.route('/')
def index():
    return static_file('index.html', root='./views')

# ------------------------------------------
# LOGIN
# ------------------------------------------
@app.post('/login')
def login():
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    user = User.get_by_email(email)

    if not user or user.senha != senha:
        return template("login_error", msg="Email ou senha incorretos")

    # salva sessão
    response.set_cookie("user_id", str(user.id), secret="CHAVE_SECRETA")

    return redirect('/home')


# ------------------------------------------
# PROTEGER ROTAS
# ------------------------------------------
def usuario_logado():
    return request.get_cookie("user_id", secret="CHAVE_SECRETA")


def proteger():
    if not usuario_logado():
        redirect('/')


# ------------------------------------------
# HOME (somente logado)
# ------------------------------------------
@app.get('/home')
def home():
    proteger()
    return template("home")


# ------------------------------------------
# LOGOUT
# ------------------------------------------
@app.get('/logout')
def logout():
    response.delete_cookie("user_id")
    return redirect('/')


# ------------------------------------------
# CRUD COMPLETO
# ------------------------------------------

# LISTAR
@app.get('/users')
def listar_usuarios():
    proteger()
    usuarios = User.get_all()
    return redirect('/')


# CADASTRAR
@app.post('/register')
def register():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    novo = User(None, nome=nome, email=email, senha=senha)
    novo.save()

    return redirect('/users')


# EDITAR (form)
@app.get('/users/edit/<id:int>')
def edit_user_form(id):
    proteger()
    user = User.get(id)
    return template('user_edit', user=user)


# EDITAR (salvar)
@app.post('/users/edit/<id:int>')
def edit_user(id):
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    user = User(id, nome, email, senha)
    user.update()

    return redirect('/users')


# DELETAR
@app.get('/users/delete/<id:int>')
def delete_user(id):
    proteger()
    User.delete(id)
    return redirect('/users')


# ------------------------------------------
# ARQUIVOS ESTÁTICOS
# ------------------------------------------
@app.route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./views')


# ------------------------------------------
# RUN
# ------------------------------------------
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)