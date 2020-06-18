var centralServer = window.location.origin;

$(function saveProfile() {
    $("form[name='settings']").validate({
        rules: {
            new_name: 'required'
        },

        submitHandler: function(form) {
            function editSucces(req) {
                window.location.reload();
            }

            requestJSON('POST', dataServer + '/api/user/edit', $(form).serialize(),  editSucces, null);
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
    requestJSON('GET', dataServer + '/api/user', null, setUserSettings, null);
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});