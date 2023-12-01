// chat bot interface

document.addEventListener('DOMContentLoaded', async () => {
    const input = document.querySelector('.entry-box input');
    const chat = document.querySelector('.chat-box');

    // get url args
    let params = new URL(document.location).searchParams;
    let room = params.get('room');

    // add to chat box
    function appendMessage(data) {
        for ([id, role, text] of data) {
            let outer = document.createElement('div');
            let inner = document.createElement('div');
            outer.setAttribute('message-id', id);
            outer.classList.add('message');
            outer.classList.add(role);
            inner.innerText = text;
            outer.appendChild(inner);
            chat.appendChild(outer);
        }
    }
    
    // history fetcher
    async function populateHistory() {
        // initiate request
        let response = await fetch('/list', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({room}),
        });

        // check return status
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // convert response to json
        let data = await response.json();
        console.log(data);
        appendMessage(data);
    }

    // send the message to the server
    async function sendMessage(prompt) {
        // initiate request
        let response = await fetch('/query', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({room, prompt}),
        });

        // check return status
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // convert response to json
        let data = await response.json();
        console.log(data);
        appendMessage(data);
    }

    // handle message
    async function handleMessage() {
        let prompt = input.value.trim();
        if (prompt.length > 0) {
            input.disabled = true;
            await sendMessage(prompt);
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
            input.disabled = false;
        }
    }

    // enter handler
    input.addEventListener('keydown', (event) => {
        if (event.keyCode === 13) {
            handleMessage();
        }
    });

    // populate history
    await populateHistory();
    chat.scrollTop = chat.scrollHeight;
});
