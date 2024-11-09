import stomp
import json
from faker import Faker

# Configuración de conexión a ActiveMQ
conn = stomp.Connection([('localhost', 8161)])
conn.connect('admin', 'admin', wait=True)

# Generador de datos falsos
fake = Faker()

def generate_customer():
    return {
        "id": fake.random_int(min=1000, max=9999),
        "name": fake.name(),
        "country": fake.country(),
        "website": fake.url()
    }

# Enviar datos a la cola "test"
def send_message():
    customer = generate_customer()
    conn.send(body=json.dumps(customer), destination='/queue/test')
    print("Enviado:", customer)

send_message()
conn.disconnect()
