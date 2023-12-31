document.addEventListener('DOMContentLoaded', function() {
  var toastContainer = document.getElementById('toast-container');
  var logo = document.getElementById('privatevibezlogo');

  const toastElements = document.querySelectorAll('.toast');

  toastElements.forEach(function(toastElement) {
    setTimeout(function() {
      var toast = new bootstrap.Toast(toastElement);
      toast.hide();
    }, 2000);
  });
});



/*
  const userSpendingDateInput = document.getElementById('user-spending-date');


  userSpendingDateInput.addEventListener('change', function(event) {
    // This function will be called when the input value changes
    const selectedDate = event.target.value;


    $.ajax({
      method: 'GET',
      url: `{% url 'rooms:get_user_by_date_spending' %}`,
      data:{
        "timestamp": selectedDate,
      },
      success: function(data) {
        var userSpending = data.data;
        var total_user_spendings = userSpending.total_user_spendings
        var user_spendings = userSpending.user_spendings
        console.log(total_user_spendings);
        console.log(user_spendings);
      
        // Create table elements
        var table = document.createElement('table');
        var thead = document.createElement('thead');
        var tbody = document.createElement('tbody');

        table.setAttribute('style', 'border-collapse: separate; border-spacing: 10px; position: sticky; top: 0; z-index: 2; ');
        thead.setAttribute('style', 'background-color: #6cc6ba;');


      
        // Create table headers (th)
        var headerRow = document.createElement('tr');
        var headers = ['Item', 'Cost', 'Note', 'Broadcaster', 'Timestamp'];
      
        headers.forEach(function(headerText) {
          var th = document.createElement('th');
          th.setAttribute('style', 'padding: 8px; position: sticky; top: 0; z-index: 2;');
          th.textContent = headerText;
          headerRow.appendChild(th);
        });
      
        thead.appendChild(headerRow);
      
        // Create table rows (tr) and data cells (td)
        user_spendings.forEach(function(obj) {
          var tr = document.createElement('tr');
          tr.setAttribute('style', 'padding: 8px;');

        const date = new Date(obj.Timestamp);

          // Format date and time
          const formattedDateTime = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;


          var data = [obj.Item, obj.Cost, obj.Note, obj.room, formattedDateTime];
      
          data.forEach(function(cellData) {
            var td = document.createElement('td');
            if (cellData === obj.room) {
              var a = document.createElement('a');
              a.setAttribute('href', `/room/${obj.room}`);
              a.textContent = cellData;
              td.appendChild(a);
            } else {
              td.textContent = cellData;
            }
            tr.appendChild(td);
          });
      
          tbody.appendChild(tr);
        });
      
        // Append thead and tbody to the table
        table.appendChild(thead);
        table.appendChild(tbody);
      
        // Append the table to the container
        var container = document.getElementById('user-spending-container');
        container.innerHTML = "";
        container.appendChild(table);

        var totalSpendings = document.getElementById('total-user-spendings');
        totalSpendings.textContent = "Total Spending: " + total_user_spendings;

      },
      
      error: function(errors) {
        console.log(errors.responseText);
        var message = "Something went wrong.";
        errorToast(message);
      }
    });
    
    
  });
*/

  if(window.location.protocol == "http:"){
    protocol = "ws";
}else if(window.location.protocol == "https:"){
    protocol = "wss";
}


  document.addEventListener('DOMContentLoaded', function() {
    var toastContainer = document.getElementById('toast-container');
    var logo = document.getElementById('privatevibezlogo');

    const toastElements = document.querySelectorAll('.toast');

    toastElements.forEach(function(toastElement) {
      setTimeout(function() {
        var toast = new bootstrap.Toast(toastElement);
        toast.hide();
      }, 2000);
    });
  });





function Accept_Invitee(user_id){
  $.ajax({
      method:'POST',
      url: "/room/accept_privatechat/",
      mimeType:"multipart/form-data",
      data:{  
              'user_id' : user_id,
              'csrfmiddlewaretoken':csrfToken,
      },
      'dataType': 'json',
      success:function(){
        
          let acceptButton = document.getElementById(`accept-button-${user_id}`);
          if (acceptButton) {
              acceptButton.style.display = "none";
              successToast("Invitation accepted!");

          }

          $("#private_chat_invites_modal").load(" #private_chat_invites_modal > *");
          $("#btn-pending-invites").load(" #btn-pending-invites > *");
          $("#fan_lists").load(" #fan_lists > *");
      },
      error:function(errors, status, xhr){
          console.log(errors.responseText);
      }
  })
}
  
  function PrivateChat_CheckBox(){
      if(document.getElementById('PrivateChat').checked){
          $.ajax({
              method:'POST',
              url: "/room/PrivateChatCheckBox/",
              mimeType:"multipart/form-data",
              data:{  
                      'Checked' : "True",
                      'csrfmiddlewaretoken':csrfToken,
              },
              'dataType': 'json',
              success:function(){
                  $("#Private_Chat_Price").load(" #Private_Chat_Price > *");
              }
          })
      
      }
      else{
          $.ajax({
              method:'POST',
              url: "/room/PrivateChatCheckBox/",
              mimeType:"multipart/form-data",
              data:{  
                      'Checked' : "False",
                      'csrfmiddlewaretoken':csrfToken,
              },
              'dataType': 'json',
              success:function(){
                  $("#Private_Chat_Price").load(" #Private_Chat_Price > *");
              }
          })
      }
  }

  function PublicChat_CheckBox(){
      if(document.getElementById('PublicChat').checked){
          $.ajax({
              method:'POST',
              url: "/room/PublicChatCheckBox/",
              mimeType:"multipart/form-data",
              data:{  
                      'Checked' : "True",
                      'csrfmiddlewaretoken':csrfToken,
              },
              'dataType': 'json',
              success:function(){
                  $("#PublicChat").load(" #PublicChat > *");
              }
          })
      
      }
      else{
          $.ajax({
              method:'POST',
              url: "/room/PublicChatCheckBox/",
              mimeType:"multipart/form-data",
              data:{  
                      'Checked' : "False",
                      'csrfmiddlewaretoken':csrfToken,
              },
              'dataType': 'json',
              success:function(){
                  $("#PublicChat").load(" #PublicChat > *");
              }
          })
      }
  }

  
function Save_Bio_nav(){
  $.ajax({
      method:'POST',
      url: "/accounts/bio_info/",
      mimeType:"multipart/form-data",
      data:{  
              'Real_Name'     : document.getElementById('Real_Name').value,
              'Age'           : document.getElementById('Age').value,
              'I_Am'          : document.getElementById('I_Am').value,
              'Interested_In' : document.getElementById('Interested_In').value,
              'Location'      : document.getElementById('Location').value,
              'Language'      : document.getElementById('Language').value,
              'Body_Type'     : document.getElementById('Body_Type').value,
              'csrfmiddlewaretoken':csrfToken,
      },
      'dataType': 'json',
      success:function(){
          $("#bio_closeButton").trigger("click");
      }
  })
}
function Save_Chat(){
  if(document.getElementById('PublicChat').checked){
      PublicChatCheck = "True"
  }else{
      PublicChatCheck = "False"
  }
  $.ajax({
      method:'POST',
      url: "/room/Chat/",
      mimeType:"multipart/form-data",
      data:{  
          'Public_Chat_Check'  : PublicChatCheck,
          'PrivateChatPrice'   : parseFloat(document.getElementById('PrivateChatPrice').value),
          'csrfmiddlewaretoken':csrfToken,
      },
      'dataType': 'json',
      success:function(data){
          console.log(data)
          successToast("Private Chat Price Saved!");

 
      }
  })
}


function Save_RoomPatterns(){
  $.ajax({
      method:'POST',
      url: " {% url 'rooms:Save_RoomPatterns' %}",
      data:{
              'Price_MMM':document.getElementById('Price_MMM_button').value,
              'Price_OHYes':document.getElementById('Price_OHYes_button').value,
              'Price_OH':document.getElementById('Price_OH_button').value,

              'Duration_MMM':document.getElementById('Duration_MMM_button').value,
              'Duration_OHYes':document.getElementById('Duration_OHYes_button').value,
              'Duration_OH':document.getElementById('Duration_OH_button').value,


              'Strength_MMM':document.getElementById('MMM-Strengths').innerHTML,
              'Strength_OH':document.getElementById('OH-Strengths').innerHTML,
              'Strength_OHYes':document.getElementById('OHYes-Strengths').innerHTML,

              'Feature_OHYes': getSelectedValues('Feature_OHYes_button'),
              'Feature_OH': getSelectedValues('Feature_OH_button'),
              'Feature_MMM': getSelectedValues('Feature_MMM_button'),

              'csrfmiddlewaretoken':csrfToken,
          },
          success:function(){
              $("#Settings_close").trigger("click");

              successToast("Room Patterns Saved!");
          }
  })
}

function getSelectedValues(selectElementId) {
let valuesArray;

switch (selectElementId) {
    case 'Feature_OHYes_button':
        valuesArray = ohyes_choices.getValue(true);
        break;
    case 'Feature_MMM_button':
        valuesArray = mmm_choices.getValue(true);
        break;
    case 'Feature_OH_button':
        valuesArray = oh_choices.getValue(true);
        break;
    default:
        const selectedOptions = document.querySelectorAll(`#${selectElementId} option:checked`);
        valuesArray = Array.from(selectedOptions).map(option => option.value);
}

// Convert array to string
return valuesArray.join(';');
}





function removeAlerts() {
  $('.alert').fadeOut(300, function() {
      $(this).remove();
  });
}

// Call the removeAlerts() function after 3 seconds (3000 milliseconds)
setTimeout(removeAlerts, 3000);



function unsubscribe() {

  $.ajax({
      method:'POST',
      url: "/accounts/unsubscribe/",
      mimeType:"multipart/form-data",
      data:{  
              'csrfmiddlewaretoken':csrfToken,
          },
          'dataType': 'json',
          success:function(data){
              console.log(data)
              var message = data.data
              successToast(message);
              $("#user-details").load(" #user-details > *");
              $("#subscription-badge").load(" subscription-badge > *");
          },
          error:function(errors){
              console.log(errors.responseText)
              var message = "Something went wrong";
              errorToast(errors.responseText)
          }

          })

}


function shakeBody() {
const body = document.body;
body.classList.add('shake-now');

// Remove the class after the animation completes to stop shaking
setTimeout(() => {
    body.classList.remove('shake-now');
}, 820); // 820ms corresponds to the duration of the shake animation
}