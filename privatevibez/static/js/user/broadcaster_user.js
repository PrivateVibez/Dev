
var useractiveSocket = null; 
var usersockets = {};

var logo = document.getElementById('privatevibezlogo');


    $("#room-stats-table").load(" #room-stats-table > *");  

    // Send visitor ID
     // Get the room ID from somewhere

    const userVisitorsSocket = new WebSocket(
        'ws://' + window.location.host + `/ws/user_visitors/${room_id}/`
    );

    userVisitorsSocket.onopen = function(e) {
        console.log('user visitor socket sent')
       
        const data = {
            user_id: user_id
        };
        userVisitorsSocket.send(JSON.stringify(data));
    };
    
    userVisitorsSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const userVisitors = data.user_visitors;

    };
    
    
    



let public_socket = new WebSocket(protocol + '://' + window.location.host + `/ws/publicChat/${room_name}/`);
public_socket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data.message;
    var username = data.username;
    var item_availed = data.item_availed;

    

    if(typeof item_availed !== 'undefined')
        {
            var user_wrapper = document.createElement('div');
            var item_availed_wrapper = document.createElement('div');
            var user = document.createElement('small');

            user_wrapper.setAttribute('class', 'text-muted d-flex justify-content-end');
            user.setAttribute('class', 'public_chat_room_message_username font-weight-bold text-dark');
            item_availed_wrapper.setAttribute('class', 'card card-body py-2 my-1 public_chat_room_message_text mb-4 ml-auto');
            item_availed_wrapper.setAttribute('style', 'border-radius: 13px; width: fit-content; background: #000000; color: #ffffff;');
            
            user.innerHTML = item_availed.user;
            user_wrapper.appendChild(user);

            item_availed_wrapper.innerHTML = `${item_availed.user} availed ` + item_availed.item;

            console.log(item_availed_wrapper);
            console.log(user_wrapper);
            var messages_element = document.getElementById('public_chat_room_messages');

            document.getElementById('public_chat_room_messages').appendChild(user_wrapper);
            document.getElementById('public_chat_room_messages').appendChild(item_availed_wrapper);


            document.getElementById('public_chat_room_messages').scrollTop = document.getElementById('public_chat_room_messages').scrollHeight;

        }




    // Add message to chat room
    else if(username === user){
        var message_element = document.createElement('div');
        message_element.setAttribute('class', 'card card-body py-2 my-1 public_chat_room_message_text mb-4 ml-auto');
        message_element.setAttribute('style', 'border-radius: 13px; width: fit-content; background: #000000; color: #ffffff;');
        message_element.innerHTML = message;

        var username_element = document.createElement('div');
        username_element.setAttribute('class', 'text-muted d-flex justify-content-end');
        var username_small = document.createElement('small');
        username_small.setAttribute('class', 'public_chat_room_message_username font-weight-bold text-dark');
        username_small.innerHTML = username;
        username_element.appendChild(username_small);

        var messages_element = document.getElementById('public_chat_room_messages');
        messages_element.appendChild(username_element);
        messages_element.appendChild(message_element);

    }
    else if(username !== user)
    {
        var message_element = document.createElement('div');
        message_element.setAttribute('class', 'card card-body py-2 my-1 public_chat_room_message_text mb-4');
        message_element.setAttribute('style', 'border-radius: 13px; width: fit-content;');
        message_element.innerHTML = message;

        var username_element = document.createElement('div');
        username_element.setAttribute('class', 'text-muted d-flex');
        var username_small = document.createElement('small');
        username_small.setAttribute('class', 'public_chat_room_message_username font-weight-bold text-dark');
        username_small.innerHTML = username;
        username_element.appendChild(username_small);

        var messages_element = document.getElementById('public_chat_room_messages');
        messages_element.appendChild(username_element);
        messages_element.appendChild(message_element);
    }

    // Scroll to bottom
    //messages_element.scrollTop = messages_element.scrollHeight;
}

// Send message
var public_chat_room_form = document.getElementById('public_chat_room_form');

if(public_chat_room_form !== null){
   
public_chat_room_form.addEventListener('submit', function(e) {
    e.preventDefault();
    var message_field = document.getElementsByName('public_chat_room_message_field')[0];
    public_socket.send(JSON.stringify({
        'message': message_field.value,
        'username': user
    }));
    message_field.value = '';
    message_field.focus();
});
}

let user_private_chat_invitation_socket = new WebSocket(protocol + '://' + window.location.host + `/ws/privateChatInvitation/${room_name}/${user}/`);


user_private_chat_invitation_socket.onopen = function(e) {
    console.log('private chat invitation socket is open')
 }


 user_private_chat_invitation_socket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var is_accepted = data.is_invitation_accepted;
  console.log(is_accepted);

  if (typeof is_accepted !== 'undefined') {
    // Your code here
    document.getElementById('pending_invitation_chat').style.display = "none";

    let privateChat = document.getElementById('nav-private-chat');
    let new_element = document.createElement('div');
    new_element.setAttribute('id', 'private_chat_room_messages');
    new_element.setAttribute('style', 'min-width: 462px; max-height: 404px; overflow: auto; padding-bottom: 25px; padding-right: 8px;');

    let privateChatContainer = `

        <div class="container-fluid p-5 mt-5">
            <div class="input-group" style="bottom: 0px; height:42px; z-index:1000; position: absolute;  left: 0px;">
                
                    <input type="text" class="form-control" name="private_chat_room_message_field" required="">
                    <div class="input-group-append">
                        <button type="button" onclick="send_private_message()" class="btn btn-primary"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-fill" viewBox="0 0 16 16">
                            <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"/>
                          </svg></button>
                    </div>
            
            </div>
        </div>`
    new_element.innerHTML = privateChatContainer;
    privateChat.appendChild(new_element);

}


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
            //messages_element.scrollTop = messages_element.scrollHeight;
            
        });
    }

    }



        // Close WebSocket on page close


  
} 




    // Send message
    var private_form = document.getElementById('private_chat_room_form');

    if(private_form !== null){
    private_form.addEventListener('submit', function(e) {
        e.preventDefault();

    });

}



window.onbeforeunload = function() {
    public_socket.close();
    user_private_chat_invitation_socket.close();
    

    const data = {
        user_id: user_id,
        leaving: true // Indicate that the user is leaving
    };
    userVisitorsSocket.send(JSON.stringify(data));

    userVisitorsSocket.close();

    private_socket.close();
}













function send_private_message() {
  var message_field = document.getElementsByName('private_chat_room_message_field')[0];
  useractiveSocket.send(JSON.stringify({
      'message': message_field.value,
      'username': user
  }));
  message_field.value = '';
  message_field.focus();
}

function hideInviteButton(){
  document.getElementById("invite_model_chat").style.display = "none";
  document.getElementById("pending_invitation_chat").style.display = "block";
}

function invite_model_chat(room_id) {
  $.ajax({
      method:'POST',
      url: "/room/invite_private_chat/",
      mimeType:"multipart/form-data",
      data:{  
              'room_id'  : room_id,
              'user_id'  : user_id,   
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(data){
            console.log(data)
            hideInviteButton();



            successToast(data.data);
          },
          error:function(errors){
              console.log(errors.responseText)

              errorToast(errors.responseText)

          }
          
      });
}

 
function Thumb_Down(){

  $.ajax({
      method:'POST',
      url: "/room/Thumbs/",
      mimeType:"multipart/form-data",
      data:{  
              'broadcaster_id'  : document.getElementById('broadcasters_id').value,
              'broadcaster'     : document.getElementById('room_username').value,
              'Thumb'           : "Down",
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(){
              $("#Thumb_button").load(" #Thumb_button > *");
          }
          })
}
function Thumb_Up(){

  $.ajax({
      method:'POST',
      url: "/room/Thumbs/",
      mimeType:"multipart/form-data",
      data:{  
              'broadcaster_id'  : document.getElementById('broadcasters_id').value,
              'broadcaster'     : document.getElementById('room_username').value,
              'Thumb'           : "Up",
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(){
              $("#Thumb_button").load(" #Thumb_button > *");
          }
          })
}

function follow(){

  $.ajax({
      method:'POST',
      url: "/room/Following/",
      mimeType:"multipart/form-data",
      data:{  
              'broadcaster_id'     : document.getElementById('broadcasters_id').value,
              'broadcaster'     : document.getElementById('room_username').value,
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(data){
              var message = data.data;
              $("#follow").load(" #follow > *");
              $("#Followers_box_refesh").load(" #Followers_box_refesh > *");

              successToast(message);
          }
          })
}
function report_button(){

  $.ajax({
      method:'POST',
      url: "/accounts/Bad_Acters_Add/",
      mimeType:"multipart/form-data",
      data:{  

              'reporty'      : document.getElementById('user_username').value,
              'reported'     : document.getElementById('room_username').value,
              'message'      : document.getElementById('Report_message').value,
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(data){
              var message = data.data;
              location.href="/"

  
          }
          })
}
function custom_button(){

  $.ajax({
      method:'POST',
      url: "/accounts/Send_Vibez/",
      mimeType:"multipart/form-data",
      data:{  

              'Vibez' : document.getElementById('amount_of_vibez_to_be_sent').value,
              'user'  : document.getElementById('users_id').value,
              'note'  : document.getElementById('send_vibez_note').value,
              'room'  : document.getElementById('broadcasters_id').value,

              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(data){
              var message = data.data;
              var user_vibez = data.vibez;
              
              document.getElementById("user_vibez").innerHTML = user_vibez;
              document.getElementById("custom_Vibez").value = '';

              successToast(message);
          },
          error:function(errors){
              errorToast(errors.responseText);
          },
          })
}


function cancel_sending_vibez()
{
  document.getElementById('left_buttons_Custom').style.display='none'
  document.getElementById('left_buttons_vibez').style.display='block'
}



function custom_change(){

  document.getElementById('left_buttons_Custom').style.display='block'
  document.getElementById('left_buttons_vibez').style.display='none'

}


function Buy_Vibez(){
  if (document.getElementById('option1').checked){
      Vibez = document.getElementById('option1').value
  }
  if (document.getElementById('option2').checked){
      Vibez = document.getElementById('option2').value
  }
  if (document.getElementById('option3').checked){
      Vibez = document.getElementById('option3').value
  }
  if (document.getElementById('option4').checked){
      Vibez = document.getElementById('option4').value
  }
  if (document.getElementById('option5').checked){
      Vibez = document.getElementById('option5').value
  }
  if (document.getElementById('option6').checked){
      Vibez = document.getElementById('option6').value
  }
  if (document.getElementById('option7').checked){
      Vibez = document.getElementById('option7').value
  }
  if (document.getElementById('option8').checked){
      Vibez = document.getElementById('option8').value
  }
  if (document.getElementById('option9').checked){
      Vibez = document.getElementById('option9').value
  }
  $.ajax({
      method:'POST',
      url: "/accounts/Buy_Vibez/",
      mimeType:"multipart/form-data",
      data:{  
              'Vibez'      : Vibez,
              'csrfmiddlewaretoken':csrf_token,
          },
          'dataType': 'json',
          success:function(data){
              var Vibez = data.data
              location.href=""
              console.log(data);
              var message = "You have successfully bought " + Vibez + " Vibez!";
              successToast(message);
          },
          errors:function(errors){
              console.log(errors.responseText)
              var message = "Something went wrong";
              errorToast(message)
          }

          })
}


function confirm_send(number,btn){

$.ajax({
  method:'POST',
  url: "/room/fav_btn_trigger_toy/",
  mimeType:"multipart/form-data",
  data:{  
          'button_type': btn,
          'user_id'    : user_id,
          'room_id'    : room_id,
          'csrfmiddlewaretoken':csrf_token,
      },
      'dataType': 'json',
      success:function(data){
          console.log(data.user_vibez);
          var message = data.data
          successToast(message);

          document.getElementById("user_vibez").innerHTML = data.user_vibez;

          document.getElementById('public_chat_room_messages').scrollTop = document.getElementById('public_chat_room_messages').scrollHeight;

        
      },
      error:function(errors){
          console.log(errors.responseText)
          var message = "Something went wrong";
          errorToast(errors.responseText)
      }

      })
}



const subscriptionButtons = document.querySelectorAll('.subscription');

// Add a click event listener to each button
subscriptionButtons.forEach(function(button) {
button.addEventListener('click', function() {
// Use 'this' to refer to the clicked button
const subscriptionType = this.getAttribute('data-subscription-type');

// Log the value to the console
console.log(subscriptionType);


$.ajax({
  method:'POST',
  url: "/accounts/avail_subscription/",
  mimeType:"multipart/form-data",
  data:{  
         
          'subscription_type'  : subscriptionType,
          'csrfmiddlewaretoken':csrf_token,
      },
      'dataType': 'json',
      success:function(data){
          var user_data = data.userdata
          var message = data.data
          
          $("#user-details").load(" #user-details > *");
          $("#subscription-badge").load(" subscription-badge > *");
          




          successToast(message);
   
        
      },
      error:function(errors){
      
          var msg = JSON.parse(errors.responseText)
          var message = "Something went wrong";
          errorToast(msg.data)
      }

      });

});
});

