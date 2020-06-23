var centralServer = window.location.origin;
var dataServer = ""

function changePassword() {
    $("form[name='changePassword']").validate({
      rules: {
        username: "required",
        password: "required",
        confirm_password: {
            required: true,
            equalTo: "$password"
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

        requestJSON('POST', dataServer + '/api/user/forgotPassword', $(form).serialize(), passwordChanged, changeFailed);
        }

    });
};

function setDataAddress(req) {
dataServer = req.data.address;
}

$(document).ready(function() {
requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});

