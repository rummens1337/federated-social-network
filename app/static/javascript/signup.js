// Validates the signup form and registers a user on the central and
// data server (selected by user).
function sign_up() {
  $("form[name='signup']").validate({
    rules: {
      username: "required",
      firstname: "required",
      lastname: "required",
      email: {
        required: true,
        email: true
      },
      password: "required",
      confirmpassword: {
        equalTo: "#password",
        required: true
      }
    },
    messages: {
      confirmpassword: "Passwords don't match"
    },

    submitHandler: function(form) {

      function registerCentral() {
        serverForm = {username:form.username.value, server_address:form.select_server.value};
        requestJSON("POST", "/api/user/register", serverForm, registerData, signupFailed);
      }

      function registerData() {
        requestJSON("POST", form.select_server.value + "/api/user/register", $(form).serialize(), signupSucces, signupFailed);
      }

      function signupSucces() {
        requestJSON("POST", form.select_server.value + "/api/mail/token", $(form).serialize(), mail_sent);
      }

      function mail_sent() {
        toggle_modal("registerUser");
        alertError("Registered account, please check your email to verify it!", 4000);
      }

      function signupFailed(response) {
        alertError(response.reason, 2000, "registerUser");
      }

      // First register the user on central to check availability of the username and IP address.
      $("#btnSubmit").attr("disabled", true);
      registerCentral();
    }
  });
}

// Gets all servers from the central database and adds them to a select div.
function loadServers() {
  document.getElementById("select_server").innerHTML = "";
  requestJSON("GET", "/api/server", null, populateServerSelect, requestError);

  function populateServerSelect(req) {
    var select = document.getElementById('select_server')
    var data = req.data.servers;

    for(i in data) {
      var server_option = document.createElement("option");
      server_option.value = data[i][1]
      server_option.textContent = data[i][0]

      select.appendChild(server_option);
    }

  }

  function requestError(req) {
    alert("Couldn't load servers...")
  }
}
