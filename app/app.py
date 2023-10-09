from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
from uuid import uuid4

import os

from flask import session
from flask_session import Session

from data import Tables, USERS
tables = Tables()

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)




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
        if user == os.environ['PRELLA_LOGIN'] and password == os.environ['PRELLA_PASSWORD']:
            login_user(USERS[id])
            return redirect('/')
    
    return render_template('login.html')


@app.route("/", methods=["GET", "POST"])
@login_required
def func():
    return render_template("index.html", order=tables.get_order(), info=tables.get_info())

#add table
@socketio.on('new table')
def newTable(data):
    info = tables.create_table(data['label'])
    if info == "error":
        socketio.emit('error', room=session['sid'])
    else:
        socketio.emit('create table', info)
        tables.saveData()

#add task
@socketio.on('new task')
def newTask(data):
    info = tables.create_task(data['label'], table_id = data['table_id'])
    if info == "error":
        socketio.emit('error', room = session['sid'])
    else:
        socketio.emit('create task', info)
        tables.saveData()

#delete table
@socketio.on('del table')
def delTable(data):
    info = tables.delete_table(data['id'])
    if info == "error":
        socketio.emit('error', room=session['sid'])
    else:
        socketio.emit('delete table', info)
        tables.saveData()

#delete task
@socketio.on('del task')
def delTask(data):
    info = tables.delete_task(data['id'], data['table_id'])
    if info == "error":
        socketio.emit('error', room = session['sid'])
    else:
        socketio.emit('delete task', info)
        tables.saveData()

#change name of table
@socketio.on('rename table')
def renameTable(data):
    status = tables.rename_table(data['id'], data['label'])
    if status == "error":
        socketio.emit('error', room = session['sid'])
    elif status != 'same':
        socketio.emit('rename table', data)
        tables.saveData()

#change name of task
@socketio.on('rename task')
def renameTask(data):
    info = tables.rename_task(data['id'], data['table_id'], data['label'])
    if info == "error":
        socketio.emit('error', room = session['sid'])
    elif info != 'same':
        socketio.emit('rename task', data)
        tables.saveData()

#change pos table
@socketio.on('change index table')
def changePosTable(data):
    table_id = data['table_id']
    oldIndex = int(data['oldIndex'])
    newIndex = int(data['newIndex'])
    if table_id in ['', 'delete']:
    	return 1
    info = tables.changeIndexTable(table_id, oldIndex, newIndex)
    if info == "error":
        socketio.emit('error', room = session['sid'])
    else:
        socketio.emit('change index table', info)
        tables.saveData()

#change pos task
@socketio.on('change index task')
def changePosTask(data):
    task_id = data['task_id']
    oldIndex = data['oldIndex']
    newIndex = data['newIndex']
    toTable = data['toTable']
    fromTable = data['fromTable']
    if toTable in ['','delete']:
    	return 1
    info = tables.changeIndexTask(task_id, int(oldIndex), int(newIndex), toTable, fromTable)
    if info == "error":
        socketio.emit('error', room=session['sid'])
    else:
        socketio.emit('change index task', info)
        tables.saveData()

@socketio.on('connect')
def connect():
    session['sid'] = request.sid
    print('#= new client =#')
'''
@socketio.on('disconnect')
def disconnect():
    print("discon!!!!!")'''

