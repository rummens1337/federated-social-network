var centralServer = window.location.origin;
var dataServer = ""

function forgotPassword() {
    $("form[name='recoverPassword']").validate({
      rules: {
        username: "required",
        email: {
          required: true,
          email: true
        },
      },

      submitHandler: function(form) {
        function setDataAddress(req) {
            dataServer = req.data.address;
        }

        requestJSON('GET', centralServer + '/api/user/address?username=' + form.username.value, null, setDataAddress, null);
      }
    });
}

