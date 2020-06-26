var centralServer = window.location.origin;
var dataServer = "";

function saveProfile() {
    $("form[name='settings']").validate({
        rules: {
            new_name: 'required',
        },

        submitHandler: function(form) {
            function editSucces() {
                window.location.reload();
            }

            function editFailed(response) {
                alertError(response.reason, 2000);
            }

            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/edit', data, editSucces, editFailed);
          }
    });
};

function setUserSettings(req) {
    document.getElementById('image_url').src = req.data.image_url;
    document.getElementById('location').value = req.data.location;
    document.getElementById('firstname').value = req.data.firstname;
    document.getElementById('lastname').value = req.data.lastname;
    document.getElementById('study').value = req.data.study;
    document.getElementById('bio').value = req.data.bio;
    document.getElementById('status').value = req.data.relationship_status;
    document.getElementById('phone_number').value = req.data.phone_number;
}

function deleteProfile() {
    function deleteDataSuccess(){
        console.log("Profile deleted from data server");
        alertError("Your profile has been deleted.");
        Cookies.delete('access_token_cookie');
        location.href = "/";
    }

    function deleteDataFail(res) {
        console.log("Delete data error: " + res.reason + "Data server: " + dataServer);
        alertError("Your profile is deleted from the central server and is now unreachable. However it is not possible to delete it from your data server. Please contact the owner of your data server.", 20000);
    }

    function deleteCentralSuccess() {
        console.log("Profile deleted from central server.");
        requestJSON("POST", dataServer + "/api/user/delete", null, deleteDataSuccess, deleteDataFail);
    }

    function deleteCentralFail() {
        alertError("Your profile could not be deleted, please try again later.", 5000);
    }

    if (confirm("Are you sure you want to delete your entire FedNet profile?")) {
        requestJSON("POST", "/api/user/delete", null, deleteCentralSuccess, deleteCentralFail);
    }
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/user', null, setUserSettings, null);
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});