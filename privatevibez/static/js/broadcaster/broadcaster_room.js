 
    let broadcaster_visitors = 0;

    var message = document.getElementById('alerts')
  
    const roomViewerSocket = new WebSocket(
        protocol + '://' + window.location.host + `/ws/room_viewer/${room_id}/`
    );

    roomViewerSocket.onopen = function(e) {
        console.log('viewer socket open');
    }

    roomViewerSocket.onmessage = function(e) {

        var data = JSON.parse(e.data);
        var is_leaving = data.is_leaving;

        console.log(data);
        console.log('viewer recieved');
        $("#room-stats-table").load(" #room-stats-table > * ");

        if (is_leaving !== undefined) {
            console.log(is_leaving);

            if (is_leaving === true) {
            
                        if (broadcaster_visitors > 0){
                        broadcaster_visitors--;
                        document.getElementById('visitors').innerHTML =  broadcaster_visitors;
                    }
  
            }

            else if(is_leaving === false) {
                broadcaster_visitors++;
                document.getElementById('visitors').innerHTML =  broadcaster_visitors;

        }

    }
}



    const roomVisitorsSocket = new WebSocket(
        protocol + '://' + window.location.host + `/ws/user_visitors/${room_id}/`
    );
    
    roomVisitorsSocket.onerror = function(error) {
        console.error("WebSocket Error: ", error);
    };


    roomVisitorsSocket.onopen = function(e) {

        console.log("WebSocket State:", roomVisitorsSocket.readyState);

        console.log("room visitor socket open")
        
        // Send a trigger message to the server
    
        roomVisitorsSocket.send(JSON.stringify({
            action: 'retrieve_visitors'
        }));
      
    };
    
    roomVisitorsSocket.onmessage = function(e) {
        let num_of_visitors = document.getElementById('visitors')
        let visitors_list = document.getElementById('visitor_list')
        const data = JSON.parse(e.data);
        const visitors = data.user_visitors;
        const item_availed = data.item_availed;

        console.log(visitors);
        
        $("#room-stats-table").load(" #room-stats-table > *");  
        $("#visitor_list").load(" #visitor_list > *");  
        document.querySelector('.msg-list-wrapper-split').scrollTop = document.querySelector('.msg-list-wrapper-split').scrollHeight;

        

        if (visitors !== undefined && Object.keys(visitors).length > 0) {
            document.getElementById('visitors').innerHTML = Object.keys(visitors).length;
        }

    };


    
const userSessionSocket = new WebSocket(
      protocol + '://' + window.location.host + `/ws/user_session/`
  );



  userSessionSocket.onopen = function(e) {
    console.log("user session online");
  }
  userSessionSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    $("#follower-details-table").load(" #follower-details-table > * ");


  }








    let fetch_broadcaster_invitation_socket = new WebSocket(protocol + '://' + window.location.host + `/ws/fetchBroadcasterPrivateChatInvitation/${room_name}/`);

    fetch_broadcaster_invitation_socket.onopen = function(e) {
        console.log('user_private_chat_invitation_socket open');

    }

    fetch_broadcaster_invitation_socket.onmessage = function(e) {
      var data = JSON.parse(e.data);
      var is_invitation_sent = data.is_invitation_sent;
      console.log(is_invitation_sent);

      if (typeof is_invitation_sent !== 'undefined') {
        // Your code here
        $("#private_chat_invites_modal").load(" #private_chat_invites_modal > *");
        $("#btn-pending-invites").load(" #btn-pending-invites > *");

        shakeBody();
    }
    
   
} 
    function generate_lovense_qrcode(){
        $.ajax({
            method:'POST',
            url: "lovense/generate_broadcaster_qrcode/",
            data: {
                'csrfmiddlewaretoken':csrf_token,
            },
            success:function(data)
            {
                console.log(data.data.qr)
                const qrCodeImg = document.getElementById('lovense_qr_code_img');
                qrCodeImg.src = data.data.qr;
                qrCodeImg.style.display = 'block'; //
            },
            errors:function(errors){
                console.log(errors.responseText)
            }
        })
    }


    function update_room_rules()
    {
        
        $.ajax({
            method: 'POST',
            url: "update_room_rules/",
            data: {
    
                'room_rules':document.getElementById('room_rules').value,
                'csrfmiddlewaretoken':csrf_token,
            },
            success:function(data)
            {
                var message = data.data;

                successToast(message);

            },
            errors:function(errors){
                console.log(errors.responseText)

                var message = "Something went wrong."

                errorToast(message);
            }
        })
    }



    function update_room_description()
    {
        
        $.ajax({
            method: 'POST',
            url: "update_room_description/",
            data: {
    
                'room_description':document.getElementById('room_description').value,
                'csrfmiddlewaretoken':csrf_token,
            },
            success:function(data)
            {
                var message = data.data;

                successToast(message);

            },
            errors:function(errors){
                console.log(errors.responseText)

                var message = "Something went wrong."

                errorToast(message);
            }
        })
    }


