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
client = messages.MessageQueue(**conf)

# routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['POST'])
def list():
    print('list')
    client.update()
    return jsonify(client.queue)

@app.route('/query', methods=['POST'])
def query():
    prompt = request.form['prompt']
    print('query:', prompt)
    client.query(prompt, block=True)
    client.update()
    return jsonify(client.queue)

# main loop
if __name__ == '__main__':
    app.run(debug=True)
