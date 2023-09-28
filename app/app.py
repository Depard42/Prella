from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
from uuid import uuid4

from flask import session
from flask_session import Session

from data import Tables
tables = Tables()

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)


class User():
    def __init__(self, id, username):
        self.id = id
        self.username = 'test'
        self.active = True
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.id
USERS = {'1': User('1','test')}

from flask_login import LoginManager, login_required
login = LoginManager()
@login.user_loader
def load_user(id):
    try:
        return USERS.get(str(id))
    except:
        return None

login.init_app(app)
login.login_view = 'login'



from flask_login import current_user, login_user
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        id = '1'
        user = request.form['username']
        password = request.form['password']
        if user == 'test' and password == 'pas':
            login_user(USERS[id])
            return redirect('/')
    
    return render_template('login.html')


@app.route("/", methods=["GET", "POST"])
@login_required
def func():
    return render_template("index.html", order=tables.order, info=tables.info)

#add table
@socketio.on('new table')
def newTable(data):
    info = tables.create_table(data['label'])
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('create table', info)
    tables.saveData()
#add task
@socketio.on('new task')
def newTable(data):
    info = tables.create_task(data['label'], table_id=int(data['table_id']))
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('create task', info)
#delete table
@socketio.on('del table')
def delTable(data):
    info = tables.delete_table(int(data['id']))
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('delete table', info)
#delete task
@socketio.on('del task')
def delTask(data):
    info = tables.delete_task(int(data['id']), int(data['table_id']))
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('delete task', info)
    tables.saveData()
#change name of table
@socketio.on('rename table')
def renameTable(data):
    info = tables.rename_table(int(data['id']), data['label'])
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('rename table', data)
    tables.saveData()
#change name of task
@socketio.on('rename task')
def renameTask(data):
    info = tables.rename_task(data['id'], data['table_id'], data['label'])
    if info == "error":
        socketio.emit('error', room=session['sid'])
    socketio.emit('rename task', data)
    tables.saveData()


@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    print('new ses')
'''
@socketio.on('disconnect')
def disconnect():
    print("discon!!!!!")'''

