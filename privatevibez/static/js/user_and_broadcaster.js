

var logo = document.getElementById('privatevibezlogo');
var toastContainer = document.getElementById('toast-container');

function successToast(message,fav_btn_element = null){
      // Create a new toast element
      var newToastElement = document.createElement('div');
      newToastElement.className = 'toast';
      newToastElement.classList.add('position-fixed');
      newToastElement.classList.add('top-25');
      newToastElement.classList.add('end-0');
      newToastElement.classList.add('mr-5');
      console.log("successToast");
      newToastElement.setAttribute('data-stackable-toast', '');
      newToastElement.setAttribute('data-delay', '5000');

      // Customize the toast content
      newToastElement.innerHTML = `
          <div class="toast-header">
              <img src=${logo.src} width="30px" height="30px" alt="">
              Notification
          </div>
          <div class="toast-body">
              ${message}
          </div>
      `;

          newToastElement.classList.add('bg-success');
          newToastElement.classList.add('p-auto');

        
         if(fav_btn_element != null)
         {
            newToastElement.appendChild(fav_btn_element);
            console.log(fav_btn_element);
         }


          // Append the new toast element to the container
          toastContainer.appendChild(newToastElement);

          

          

          // Initialize and show the toast
          var newToast = new bootstrap.Toast(newToastElement);
          newToast.show();
      
}
function errorToast(message){
      // Create a new toast element
      var newToastElement = document.createElement('div');
      newToastElement.className = 'toast';
      newToastElement.classList.add('position-fixed');
      newToastElement.classList.add('top-25');
      newToastElement.classList.add('end-0');
      newToastElement.classList.add('mr-5');
      newToastElement.setAttribute('data-stackable-toast', '');
      newToastElement.setAttribute('data-delay', '2000');

      // Customize the toast content
      newToastElement.innerHTML = `
          <div class="toast-header">
              <img src=${logo.src} width="30px" height="30px" alt="">
              Notification
          </div>
          <div class="toast-body">
              ${message}
          </div>
      `;

          newToastElement.classList.add('bg-danger');

          // Append the new toast element to the container
          toastContainer.appendChild(newToastElement);

          // Initialize and show the toast
          var newToast = new bootstrap.Toast(newToastElement);
          newToast.show();
      
}


function generate_lovense_qrcode(){
    $.ajax({
        method:'POST',
        url: "lovense/generate_broadcaster_qrcode/",
        data: {
            'csrfmiddlewaretoken':"{{csrf_token}}",
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

