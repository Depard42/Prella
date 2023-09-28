from app.app import app, socketio

socketio.run(app, debug="True",host="0.0.0.0",port=8080)