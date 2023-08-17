


function successToast(message){
      // Create a new toast element
      var newToastElement = document.createElement('div');
      newToastElement.className = 'toast';
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

          newToastElement.classList.add('bg-success');

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
