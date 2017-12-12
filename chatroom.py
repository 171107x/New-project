from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdxswedfrcswqsax12redsx'
socketio = SocketIO( app )


@app.route('/chat')
def hello():
  return render_template( '/chat.html' )


def messagereceived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messagereceived())

if __name__ == '__main__':
  socketio.run( app, debug = True )