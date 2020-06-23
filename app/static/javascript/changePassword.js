var centralServer = window.location.origin;
var dataServer = ""

function change() {
    $("form[name='changePassword']").validate({
      rules: {
        password: "required",
        confirm_password: {
            required: true,
            equalTo: "#password"
        }
      },

      submitHandler: function(form) {
        function changeFailed(req) {
            alertError(req.reason, 2000);
        }

        function passwordChanged() {
            alert("Password changed")
        }

        requestJSON('POST', dataServer + '/api/mail/confirm_forgotpass', $(form).serialize(), passwordChanged, changeFailed);
        }

    });
};

function setDataAddress(req) {
    dataServer = req.data.address;
}

$(document).ready(function() {
    const queryString = window.location.search;
    const urlParam = new URLSearchParams(queryString);
    const token = urlParam.get('token')
    const username = urlParam.get('username')
    document.getElementById('token').value = token

    requestJSON('GET', centralServer + '/api/user/address?username=' + username, null, setDataAddress, function(req) {
        alertError(req.reason, 2000);
    })
});