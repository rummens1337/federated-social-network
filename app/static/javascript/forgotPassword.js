var centralServer = window.location.origin;
var dataServer = ""

function forgotPassword() {
    $("form[name='recoverPassword']").validate({
      rules: {
        username: "required"
      },

      submitHandler: function(form) {
        function setDataAddress(req) {
            dataServer = req.data.address;
            requestJSON('POST', dataServer + '/api/mail/forgotpass', $(form).serialize(), mail_sent, mailFailed)
        }

        function mail_sent() {
            toggle_modal("recoverPassword");
            alertError("Mail sent, please check your email to change password!", 4000);
        }

        function mailFailed(response) {
            alertError(response.reason, 2000);
        }

        requestJSON('GET', centralServer + '/api/user/address?username=' + form.username.value, null, setDataAddress, null);
      }
    });
}

