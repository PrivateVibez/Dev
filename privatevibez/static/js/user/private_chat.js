


let private_socket = new WebSocket(protocol + '://' + window.location.host + `/ws/privateChatBroc/${room_name}/${user}/`);

let is_initialized = false;
useractiveSocket = private_socket;
private_socket.onopen = function(e) {
    console.log('private chat socket is open');
}

    private_socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var messages;

        if (is_initialized === true) {
            
        messages = [data.data];
        } else {
        messages = data.data;
        }

        (is_initialized) ? console.log('private chat socket is open') : is_initialized = true;

        // Add message to chat room
        
        
        console.log(messages);
        if(typeof messages !== undefined)
        {
        messages.forEach(function (messageText) {
            var from = messageText.From;
            var to = messageText.To;
            var message = messageText.Message;
            
            // Now you can use 'from', 'to', and 'messageText' for processing or displaying the message.
            console.log(`From: ${from}, To: ${to}, Message: ${message}`);

            if(from !== undefined && from === user){
                var message_element = document.createElement('div');
                message_element.setAttribute('class', 'card card-body py-2 my-1 private_chat_room_message_text mb-4 ml-auto');
                message_element.setAttribute('style', 'border-radius: 13px; width: fit-content; background: #000000; color: #ffffff;');
                message_element.innerHTML = message;
    
                var username_element = document.createElement('div');
                username_element.setAttribute('class', 'text-muted d-flex justify-content-end');
                var username_small = document.createElement('small');
                username_small.setAttribute('class', 'private_chat_room_message_username font-weight-bold text-dark');
                username_small.innerHTML = from;
                username_element.appendChild(username_small);
    
                var messages_element = document.getElementById('private_chat_room_messages');
                messages_element.appendChild(username_element);
                messages_element.appendChild(message_element);
            }else if(from !== undefined && from !== user) {
                var message_element = document.createElement('div');
                message_element.setAttribute('class', 'card card-body py-2 my-1 private_chat_room_message_text mb-4');
                message_element.setAttribute('style', 'border-radius: 13px; width: fit-content;');
                message_element.innerHTML = message;
    
                var username_element = document.createElement('div');
                username_element.setAttribute('class', 'text-muted d-flex');
                var username_small = document.createElement('small');
                username_small.setAttribute('class', 'private_chat_room_message_username font-weight-bold text-dark');
                console.log(typeof(to));
                username_small.innerHTML = from;
                username_element.appendChild(username_small);
    
                var messages_element = document.getElementById('private_chat_room_messages');
                messages_element.appendChild(username_element);
                messages_element.appendChild(message_element);
            }
    
            // Scroll to bottom
           // messages_element.scrollTop = messages_element.scrollHeight;
            
        });
    }

    }




