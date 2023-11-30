document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.querySelector('.entry-box button');
    const messageInput = document.querySelector('.entry-box input');
    const chatBox = document.querySelector('.chat-box');

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = ''; // Clear the input field
        }
    });

    function sendMessage(message) {
        // Send the message to the server
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'user_message': message,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(responseMessage => {
            // Handle the response from the server
            appendMessage(responseMessage);
        })
        .catch(error => {
            console.error('Fetch error: ', error);
        });
    }

    function appendMessage(data) {
        // Display the bot's response
        console.log(data);

        // turn list of lists into divs
        for (row of data.toReversed()) {
            for (text of row) {
                let col = document.createElement('div');
                col.innerText = text;
                chatBox.appendChild(col);
            }
        }

        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
