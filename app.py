import os
import time
import openai

from openai import OpenAI
from flask import Flask, render_template, request, jsonify, send_file

thread_id='thread_Ge20kslclNBsNheDJXcMDNnq'
assist_id= 'asst_oRP7qsyru69o9LtYNlAP00Bt'

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

client = openai.OpenAI()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    response = generate_chat_response(user_message)
    return jsonify(response)

def generate_chat_response(user_message):
    # create message
    response = openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message,
    )

    # run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assist_id,
    )

    # wait for completion
    for _ in range(20):
        # get run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # check for completion
        print(run)
        if run.status == 'completed':
            break
        else:
            time.sleep(2)


    # get messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # parse messages
    print(messages)
    contents = [
        [c.text.value for c in d.content]
        for d in messages.data
    ]
    print(contents)
    return contents

if __name__ == '__main__':
    app.run(debug=True)
