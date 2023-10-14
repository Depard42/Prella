from app.app import app, socketio

socketio.run(app, allow_unsafe_werkzeug=True, debug=True, host="0.0.0.0", port=80)