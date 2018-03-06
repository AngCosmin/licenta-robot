import ConfigParser
import websocket
import thread
import json
from controllers.MotorsController import MotorsController
from controllers.RelayController import RelayController

ws = None

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()

    motors = MotorsController()
    relay = RelayController()

    try:
        config.read('./config.cfg')

        server_ip = config.get('Websocket', 'server_ip')
        server_port = config.get('Websocket', 'server_port')

        print 'Connecting to ' + server_ip + ':' + server_port + '...'

        websocket.enableTrace(True)
        ws = websocket.WebSocketApp('ws://' + server_ip + ':' + server_port)

        ws.on_open = on_open
        ws.on_message = on_message
        ws.on_error = on_error
        ws.on_close = on_close

        ws.run_forever()
    except Exception as e:
        print e

def on_open(self, ws):
    print 'Connection is now open!'
    ws.send(json.dumps({'event': 'connection', 'client': 'Robot'}));

def on_error(self, ws, error):
    print error

def on_close(self, ws):
    motors.clean();
    print 'Connection is now closed!'

def on_message(self, ws, message):
    try:
        message = json.loads(message)
        event = message['event']
        
        if event == 'move':
            motorLeftSpeed = message['motorLeftSpeed']
            motorRightSpeed = message['motorRightSpeed']
            
            motors.move_motors(motorLeftSpeed, motorRightSpeed)
        elif event == 'turn_motors':
            if message['status'] == 'on':
                relay.start()
            else:
                relay.stop()
    except Exception as e:
        print e