from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/person', methods=['POST'])
def receive_person():
    data = request.json
    print("Datos recibidos:", data)
    return jsonify({"status": "received", "data": data}), 201

if __name__ == '__main__':
    app.run(port=5000)
