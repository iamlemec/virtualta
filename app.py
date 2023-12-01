# chat bot

import toml
from flask import Flask, render_template, request, jsonify

import messages

# create app
app = Flask(
    __name__, static_folder='static', template_folder='templates'
)

# create client
conf = toml.load('config.toml')
opts = conf['options']
clients = {
    k: messages.MessageQueue(**v, **opts) for k, v in conf['rooms'].items()
}

# routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['POST'])
def list():
    room = request.form['room']
    print(f'list [{room}]')

    if room not in clients:
        print(f'room [{room}] not found')
        return jsonify([])
    else:
        client = clients[room]

    client.update()
    return jsonify(client.queue)

@app.route('/query', methods=['POST'])
def query():
    room = request.form['room']
    prompt = request.form['prompt']
    print(f'query [{room}]: {prompt}')

    if room not in clients:
        print(f'room [{room}] not found')
        return jsonify([])
    else:
        client = clients[room]

    client.query(prompt, block=True)
    client.update()
    return jsonify(client.queue)

# main loop
if __name__ == '__main__':
    app.run(debug=True)
