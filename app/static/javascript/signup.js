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

        function signupSucces() {

          // requestJSON("POST", location.origin + "/server/register", $(form).serialize(), signupSucces, signupFailed);
          if(!alert('You have been succesfully registered!')){window.location = "/";}
        }

        function signupFailed(XMLHttpRequest, textStatus, errorThrown) {
          alert("Failed to register.")
        }

        function register() {
          requestJSON("POST", form.select_server.value + "/api/user/register", $(form).serialize(), signupSucces, signupFailed);
        }

        register();
    }
  });
}

$(document).ready( function() {
  requestJSON("GET", window.location.origin + "/api/server", null, populateServerSelect, requestError);

  function populateServerSelect(req) {
    var select = document.getElementById('select_server')
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
});