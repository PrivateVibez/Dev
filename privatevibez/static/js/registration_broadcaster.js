
const loadingScreen = document.getElementById('loading');
    
// Show the loading screen before making the AJAX request
function showLoadingScreen() {
    loadingScreen.style.display = 'block';
}

// Hide the loading screen after the AJAX request is complete
function hideLoadingScreen() {
    loadingScreen.style.display = 'none';
}


function ID_Next(){
  showLoadingScreen();
    $.ajax({
        method:'POST',
        url: "/accounts/saveBroacasterInfo/",
        mimeType:"multipart/form-data",
        data:{  
                'first_name': document.getElementById('firstName').value,
                'last_name': document.getElementById('lastName').value,
                'Birth_date': document.getElementById('BirthDate').value,
                'csrfmiddlewaretoken':"{{csrf_token}}",
            },
            'dataType': 'json',
            success:function(){
              document.getElementById('info_box').style.display='none'
              document.getElementById('id_card_box').style.display='block'

              hideLoadingScreen();
              }
    })
}

function Stumiting_id_words(){  
    showLoadingScreen();
    const file = document.getElementById('Id_Card_File').files[0];
    const id_card_file = new FormData();
    id_card_file.append('file', file);
    $.ajax({
        method:'POST',
        url: "/accounts/saveBroacasterId/",
        mimeType:"multipart/form-data",
        data: id_card_file,
        processData: false,
        contentType: false,
        success:function(data){
            var message = data;
              
              document.getElementById('Registration_words').style.display='none'
              document.getElementById('id_card_box').style.display='none'
              document.getElementById('Not_Shown_questions').style.display='none'
              document.getElementById('Stumiting_id_words').style.display='block'
              
              hideLoadingScreen();
            

            },
        error: function(error) {

          hideLoadingScreen();
          errorToast(error.responseText);
          console.log(error.responseText);
        }
    })
}

function Next_Profile_Image(){
    
    document.getElementById('Registration_words').style.display='none'
    document.getElementById('Stumiting_id_words').style.display='none'
    document.getElementById('Shown_questions').style.display='block'
    document.getElementById('Profile_pic_words').style.display='block'
    document.getElementById('profile_pic_box').style.display='block'

}

function Next_bio(){
    const file = document.getElementById('Profile_Pic').files[0];
    const Profile_Pic = new FormData();
    Profile_Pic.append('file', file);
    $.ajax({
        method:'POST',
        url: "/accounts/Profile_Pic/",
        mimeType:"multipart/form-data",
        data: Profile_Pic,
        processData: false,
        contentType: false,
        success:function(){
            document.getElementById('bio_box').style.display='block'
            document.getElementById('bio_words').style.display='block'
            document.getElementById('Profile_pic_words').style.display='none'
            document.getElementById('profile_pic_box').style.display='none'
            hideLoadingScreen();
            }
    })
}

let cropper;

function readImage(input) {

    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        var image = document.createElement('img');
        image.src = e.target.result;

        // Set the width of the image
        image.style.width = '400px';

        var imageContainer = document.getElementById('profile_wrapper');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(image);

        cropper = new Cropper(image, {
          aspectRatio: 16 / 9,
          crop(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
          },
        });
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

  var imageInput = document.getElementById('Profile_Pic');

  imageInput.addEventListener('change', function () {
    readImage(this);
  });




function done(){
      showLoadingScreen();
      const croppedCanvas = cropper.getCroppedCanvas();
      croppedCanvas.toBlob(function (blob) {
        // Create a new FormData object
        const formData = new FormData();
  
        // Append the cropped image Blob to the FormData object
        formData.append('cropped_image', blob, 'cropped_image.jpg');
  
        // Append other form data fields to the FormData object
        formData.append('Real_Name', document.getElementById('firstName').value);
        formData.append('Age', document.getElementById('Age').value);
        formData.append('promotion_code', document.getElementById('promotion_code').value);
        formData.append('I_Am', document.getElementById('I_Am').value);
        formData.append('Tab', document.getElementById('tab').value);
        formData.append('Interested_In', document.getElementById('Interested_In').value);
        formData.append('Location', document.getElementById('Location').value);
        formData.append('Language', document.getElementById('Language').value);
        formData.append('Body_Type', document.getElementById('Body_Type').value);
        formData.append('csrfmiddlewaretoken', "{{csrf_token}}");
  
        // Send the data via the AJAX POST request
        $.ajax({
          method: 'POST',
          url: "/accounts/bio_info/",
          data: formData,
          dataType: 'json',
          processData: false, // Prevent jQuery from processing the data
          contentType: false, // Prevent jQuery from setting content type
          success: function () {
            document.getElementById('bio_box').style.display = 'none'
            document.getElementById('bio_words').style.display = 'none'
            document.getElementById('Shown_questions').style.display = 'none'
            document.getElementById('Done_box').style.display = 'block'

            hideLoadingScreen();
          },
          error: function (xhr, status, error) {
            console.error('Error sending the AJAX request:', error.responseText);
          }
        });
      },  'image/jpeg' );
  }
  


function Add_Menu_item(){
    $.ajax({
        method:'POST',
        url: "/room/Menu_item/",
        mimeType:"multipart/form-data",
        data:{  
                'Vibez'     : document.getElementById('Vibez').value,
                'Menu_Name' : document.getElementById('Menu_Name').value,
                'Menu_Time' : document.getElementById('Menu_Time').value,
                'csrfmiddlewaretoken':"{{csrf_token}}",
            },
            'dataType': 'json',
            success:function(){
                document.getElementById("Vibez").value = '';
                document.getElementById("Menu_Name").value = '';
                document.getElementById("Menu_Time").value = '';
                $( "#text_menu_target" ).load(window.location.href + " #text_menu_target" );
            }
            })


    
}
function Next_dice(){
    document.getElementById('Menu_box').style.display='none'
    document.getElementById('Menu_words').style.display='none'
    document.getElementById('Menu_small_words').style.display='none'
    document.getElementById('Dice_box').style.display='block'
    document.getElementById('Dice_words').style.display='block'
    document.getElementById('Dice_small_words').style.display='block'

}


