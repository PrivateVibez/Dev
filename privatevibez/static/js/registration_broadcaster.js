
function ID_Next(){
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
              }
    })
}

function Stumiting_id_words(){
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
        success:function(){
            document.getElementById('Registration_words').style.display='none'
            document.getElementById('id_card_box').style.display='none'
            document.getElementById('Not_Shown_questions').style.display='none'
            document.getElementById('Stumiting_id_words').style.display='block'

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
        
            }
    })
}
function Next_Menu(){

    $.ajax({
        method:'POST',
        url: "/accounts/bio_info/",
        mimeType:"multipart/form-data",
        data:{  
                'Real_Name'     : document.getElementById('firstName').value,
                'Age'           : document.getElementById('Age').value,
                'I_Am'          : document.getElementById('I_Am').value,
                'Tab'           : document.getElementById('tab').value,
                'Interested_In' : document.getElementById('Interested_In').value,
                'Location'      : document.getElementById('Location').value,
                'Language'      : document.getElementById('Language').value,
                'Body_Type'     : document.getElementById('Body_Type').value,
                'csrfmiddlewaretoken':"{{csrf_token}}",
            }
            ,
            'dataType': 'json',
            success:function(){
                document.getElementById('Menu_box').style.display='block'
                document.getElementById('Menu_words').style.display='block'
                document.getElementById('Menu_small_words').style.display='block'
                document.getElementById('bio_box').style.display='none'
                document.getElementById('bio_words').style.display='none'
                document.getElementById('Shown_questions').style.display='none'
                

            }
         
            })
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
function Done(){
    $.ajax({
        method:'POST',
        url: "/room/Dice_items/",
        mimeType:"multipart/form-data",
        data:{  
                '1_dice_Name'  : document.getElementById('1_dice_Name').value,
                '1_dice_Time'  : document.getElementById('1_dice_Time').value,

                '2_dice_Name'  : document.getElementById('2_dice_Name').value,
                '2_dice_Time'  : document.getElementById('2_dice_Time').value,

                '3_dice_Name'  : document.getElementById('3_dice_Name').value,
                '3_dice_Time'  : document.getElementById('3_dice_Time').value,

                '4_dice_Name'  : document.getElementById('4_dice_Name').value,
                '4_dice_Time'  : document.getElementById('4_dice_Time').value,

                '5_dice_Name'  : document.getElementById('5_dice_Name').value,
                '5_dice_Time'  : document.getElementById('5_dice_Time').value,

                '6_dice_Name'  : document.getElementById('6_dice_Name').value,
                '6_dice_Time'  : document.getElementById('6_dice_Time').value,

                'csrfmiddlewaretoken':"{{csrf_token}}",
            },
            'dataType': 'json',
            success:function(){
                document.getElementById('Done_box').style.display='block'
                document.getElementById('Dice_box').style.display='none'
                document.getElementById('Dice_words').style.display='none'
                document.getElementById('Dice_small_words').style.display='none'
            }
            })



}






