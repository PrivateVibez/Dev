const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log(data)
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `<div style="width: 100%; display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: end; text-align: right; padding: 10px 10px 5px 0px;">
              <div style="display: flex; font-size: 14px; background: lightgoldenrodyellow;; padding: 8px; border-radius: 4px;">${data.message}</div>
          </div>`
    }else{
        document.querySelector('#chat-body').innerHTML += `<div style="width: 100%; display: flex; flex-direction: row; align-items: center; justify-content: start; text-align: left; padding: 10px 5px 0px 10px;">
              <div class="textcircle" >
                  ${data.username.slice(0,2)}
              </div>
              <div style="width: calc(100% - 40px); display: flex; flex-wrap: wrap;">
                  <div style="display: flex; font-size: 14px; background: lightgoldenrodyellow;margin-left: 7px; padding: 8px; border-radius: 4px;">${data.message}</div>
              </div>
          </div>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username
    }));

    message_input.value = '';
}