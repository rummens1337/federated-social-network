var centralServer = window.location.origin;

$(function saveProfile() {
    $("form[name='settings']").validate({
        rules: {
            new_name: 'required'
        },

        submitHandler: function(form) {
            function editSucces(req) {
              if(!alert('Settings editted')){window.location.reload();}
            }

            function editFailed(XMLHttpRequest, textStatus, errorThrown) {
              alert("Failed to edit settings.")
            }

            requestJSON('POST', dataServer + '/api/user/edit?username=' + username, $(form).serialize(), editSucces, editFailed);
          }
    });
});

function setUserSettings(req) {
    document.getElementById('location').value = req.data.location;
    document.getElementById('name').value = req.data.name;
    document.getElementById('study').value = req.data.study;
}

function setDataAddress(req) {
    dataServer = req.data.address;
    username = req.data.username;
    requestJSON('GET', dataServer + '/api/user?username=' + username, null, setUserSettings, null);
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});