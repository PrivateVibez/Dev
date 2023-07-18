function Approve_Broactser(){
    $.ajax({
        method:'POST',
        url: "/staff/ID_stat/",
        mimeType:"multipart/form-data",
        data:{  
                'Status': 'Approve',
                'csrfmiddlewaretoken':"{{csrf_token}}",
            },
            'dataType': 'json',
            success:function(){
              }
    })
}
