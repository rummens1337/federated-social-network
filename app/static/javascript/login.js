function validateAccount() {
    $("form[name='login']").validate({
      rules: {
        username: {
          required: true,
        },
        password: {
          required: true,
        }
      },
      messages: {
        username: "Please enter a valid username",

        password: {
          required: "Please enter password",
        }

      },

      submitHandler: function(form) {
        // TODO: HASH PASSWORD
        var username = $("#username").val();

        function loginFailed(req) {
          alertError(req.reason, 2000);
        }

        function verifyLogin(req) {
          if (req.data.hasOwnProperty("token")) {
            // alertError("Login success", 1000)
            // Cookies.set('access_token_cookie', req.data.token);
            // alert(req.data.token)
            Cookies.set('access_token_cookie', req.data.token);
            window.location = "/";

          } else {
            loginFailed()
          }
        }

        function login(req) {
          dataServer = req.data.address;
          requestJSON('POST', dataServer + '/api/user/login', $(form).serialize(), verifyLogin, loginFailed);
        }

        // TODO set central server in API
        requestJSON('GET', '/api/user/address?username=' + username, null, login, loginFailed);
      }
    });
  }

  function validatePassword() {
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
        alert('..')
        //form.submit();
      }
    });
  }

// $(document).ready( function() {
//   let params = new URLSearchParams(window.location.search)

//   if (params.has('message')) {
//     let param = params.get('message');

//     if (param == "registration_complete") {
//       alertError("Registration Complete, you can now log in!", 2000);
//     }
//   }
// });