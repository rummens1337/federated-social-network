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

function forgotUsername() {
  $("form[name='recoverUsername']").validate({
    rules: {
      sever: "required",
      email: {
        required: true,
        email: true
      }
    },

    submitHandler: function(form) {
      function mail_sent() {
        toggle_modal("recoverUsername");
        alertError("Mail sent, please check your email to see username!", 4000);
      }

      function mailFailed(response) {
        alertError(response.reason, 2000);
      }

      requestJSON('POST', form.server.value + '/api/mail/forgot_username', $(form).serialize(), mail_sent, mailFailed)
    }

  });
}


function loadServersForgot() {
  document.getElementById("select_server2").innerHTML = "";
  requestJSON("GET", "/api/server", null, populateServerSelect, requestError);

  function populateServerSelect(req) {
    var select = document.getElementById('select_server2')
    var data = req.data.servers;
    console.log(req);

    for(i in data) {
      var server_option = document.createElement("option");
      console.log(i)
      server_option.value = data[i][1]
      server_option.textContent = data[i][0]

      select.appendChild(server_option);
    }

  }

  function requestError(req) {
    alert("Couldn't load servers...")
  }
}

