var centralServer = window.location.origin;

function changePassword() {
    $("form[name='password']").validate({
        rules: {
            oldPassword: "required",
            newPassword: "required",
            confirmPassword: {
                required: true,
                equalTo: "#newPassword"
            }
        },

        submitHandler: function(form) {
            function changeFailed(req) {
                alertError(req.reason, 2000);
            }

            function passwordChanged() {
                alert("Password changed")
                window.location.reload();
            }

            requestJSON('POST', dataServer + '/api/user/password', $(form).serialize(), passwordChanged, changeFailed);
            }

    });
};

function setDataAddress(req) {
    dataServer = req.data.address;
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});