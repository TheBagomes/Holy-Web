from bottle import Bottle, run, static_file, request, redirect, template, response
from models.user import User
from database import criar_tabelas
from bottle.ext.websocket import GeventWebSocketServer, websocket
import json

app = Bottle()

# Lista de conexões WebSocket ativas
clients = set()

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
# CRUD
# ------------------------------------------

@app.post('/register')
def register():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
    senha = request.forms.get('senha')

    novo = User(None, nome=nome, email=email, senha=senha)
    novo.save()

    return redirect('/')

# ------------------------------------------
# WEBSOCKET DO CHAT
# ------------------------------------------
@app.route('/ws', apply=[websocket])
def websocket_handler(ws):

    # pegar usuário pelo cookie
    user_id = request.get_cookie("user_id", secret="CHAVE_SECRETA")
    user = User.get(user_id)

    if not user:
        ws.close()
        return

    clients.add(ws)
    print(f"Cliente conectado: {user.nome}")

    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break

            data = json.loads(msg)

            # mensagem final a ser enviada
            mensagem_formatada = {
                "username": user.nome,
                "message": data["message"],
                "time": data["time"]
            }

            # enviar para todos
            for client in list(clients):
                try:
                    mensagem_formatada["isMine"] = (client == ws)
                    client.send(json.dumps(mensagem_formatada))
                except:
                    clients.remove(client)

    finally:
        clients.remove(ws)
        print(f"{user.nome} desconectou")

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
    run(app, host='localhost', port=8080,
        server=GeventWebSocketServer, debug=True, reloader=True)
