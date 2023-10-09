from app.app import app, socketio
import os

os.system('source /etc/environment')
socketio.run(app, allow_unsafe_werkzeug=True, debug="False",host="0.0.0.0",port=8123)