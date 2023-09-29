from app.app import app, socketio

socketio.run(app, debug="False",host="0.0.0.0",port=8080)