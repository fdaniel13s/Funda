import stomp
import json

class Listener(stomp.ConnectionListener):
    def on_message(self, headers, message):
        customer = json.loads(message)
        print("Recibido:", customer)

# Configuración de conexión a ActiveMQ
conn = stomp.Connection([('localhost', 8161)])
conn.set_listener('', Listener())
conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination='/queue/test', id=1, ack='auto')

input("Presiona Enter para finalizar...\n")
conn.disconnect()