 $.ajax
    ({
            url: "http://127.0.0.1:5000/user",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({
                'username': $("#username").val(),
                'password': $("#password").val()
            }),
            type: "GET",
            dataType: "json",
            error: function (e) {
            },
            success: function (resp) {
                if (resp.status == 'ok') {
                    if(resp.message == 'therapist'){
                        window.location.replace('Options.html')
                    }
                    else{
                        window.location.replace('Options2.html')
                    }
                }
                else {

                }

            }
    });