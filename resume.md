# CRM Marketing Module - Integration Practice

A messaging environment based on ActiveMQ where Python and Java applications communicate through a message queue named `"test"`. The project includes a Python REST service for receiving and storing information.

## Prerequisites

- [ActiveMQ](https://activemq.apache.org/)
- [Python 3](https://www.python.org/downloads/)
- Java JDK (configured in PATH)
- Python dependencies:
  ```bash
  pip install stomp-py faker Flask
  ```

## ActiveMQ Setup

1. Start ActiveMQ and access the admin console at `http://localhost:8161/admin`

   - Default credentials: admin/admin
2. Create the `test` queue:

   - Navigate to Destinations > Queues
   - Create a new queue named "test"

   Alternatively, configure the queue in `activemq.xml` (in ActiveMQ's conf directory):

   ```xml
   <destinations>
       <queue physicalName="test"/>
   </destinations>
   ```

## Components

### Python Components

#### SenderP.py

Generates and sends fake customer data to the ActiveMQ queue.

```python
import stomp
import json
from faker import Faker

conn = stomp.Connection([('localhost', 61613)])
conn.connect('admin', 'admin', wait=True)

fake = Faker()

def generate_customer():
    return {
        "id": fake.random_int(min=1000, max=9999),
        "name": fake.name(),
        "country": fake.country(),
        "website": fake.url()
    }

def send_message():
    customer = generate_customer()
    conn.send(body=json.dumps(customer), destination='/queue/test')
    print("Sent:", customer)

send_message()
conn.disconnect()
```

#### ListenerP.py

Listens to the queue and processes received messages.

```python
import stomp
import json

class Listener(stomp.ConnectionListener):
    def on_message(self, headers, message):
        customer = json.loads(message)
        print("Received:", customer)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', Listener())
conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination='/queue/test', id=1, ack='auto')

input("Press Enter to exit...\n")
conn.disconnect()
```

### Java Components

#### SenderJ.java

Sends messages to the ActiveMQ queue.

```java
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;

public class SenderJ {
    public static void main(String[] args) throws JMSException {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://localhost:61616");
        Connection connection = factory.createConnection("admin", "admin");
        connection.start();

        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Destination destination = session.createQueue("test");

        MessageProducer producer = session.createProducer(destination);
        TextMessage message = session.createTextMessage("Sending message from Java SenderJ");
        producer.send(message);

        System.out.println("Message sent: " + message.getText());
        session.close();
        connection.close();
    }
}
```

#### ReceiverJ.java

Listens to the queue and receives messages.

```java
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;

public class ReceiverJ {
    public static void main(String[] args) throws JMSException {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://localhost:61616");
        Connection connection = factory.createConnection("admin", "admin");
        connection.start();

        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Destination destination = session.createQueue("test");

        MessageConsumer consumer = session.createConsumer(destination);
        Message message = consumer.receive();

        if (message instanceof TextMessage) {
            TextMessage textMessage = (TextMessage) message;
            System.out.println("Message received: " + textMessage.getText());
        }

        session.close();
        connection.close();
    }
}
```

### REST Service (rest_service.py)

Python REST service that receives customer data.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/person', methods=['POST'])
def receive_person():
    data = request.json
    print("Data received:", data)
    return jsonify({"status": "received", "data": data}), 201

if __name__ == '__main__':
    app.run(port=5000)
```

## Testing

### Test REST Endpoint

```bash
curl -X POST "http://localhost:5000/person" \
     -H "Content-Type: application/json" \
     -d '{"id": 1234, "name": "John Doe", "country": "Peru", "website": "http://example.com"}'
```

## Architecture

The system consists of the following components:

- CRM System (Marketing and Sales modules)
- ActiveMQ (message broker)
- Python components (SenderP.py and ListenerP.py)
- Java components (SenderJ.java and ReceiverJ.java)
- REST Service (/person endpoint)

## Notes

- ActiveMQ runs on:
  - Port 61613 for Python connections
  - Port 61616 for Java connections
- Document any issues encountered and their solutions
- Include screenshots of the ActiveMQ console and application terminals
- Create a C4 container diagram showing the system architecture

This setup provides a functional messaging environment with ActiveMQ and a REST service for practicing distributed application integration.
