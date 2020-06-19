var centralServer = window.location.origin;

function saveProfile() {
    $("form[name='settings']").validate({
        rules: {
            new_name: 'required'
        },

        submitHandler: function(form) {
            function editSucces() {
                window.location.reload();
            }

            function editFailed(response) {
                alertError(response.reason, 2000);
            }

            var data = new FormData(form)
            // alert("here");
            // console.log(data);

            requestJSON2('POST', dataServer + '/api/user/edit', data, editSucces, editFailed);
          }
    });
};
function requestJSON2(type, url, data=null, success=null, error=null) {
    var token = Cookies.get('access_token_cookie');
    var headers = {};
    if (token != null) headers = { 'Authorization' : 'Bearer ' + token };

    $.ajax({
        headers: headers,
        type: type,
        url: url,
        processData: false,
        contentType: false,
        data: data,
        crossDomain: true,
        success: function(req) {
            if (req.hasOwnProperty("data")) success(req);
            else error(req);
        },
        error: error
    });
};


function setUserSettings(req) {
    document.getElementById('image_url').src = req.data.image_url;
    document.getElementById('location').value = req.data.location;
    document.getElementById('firstname').value = req.data.firstname;
    document.getElementById('lastname').value = req.data.lastname;
    document.getElementById('study').value = req.data.study;
    document.getElementById('bio').value = req.data.bio;
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/user', null, setUserSettings, null);
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});