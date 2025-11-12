from bottle import Bottle, run
from app.controllers import application

app = Bottle()
app.merge(application.app)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
