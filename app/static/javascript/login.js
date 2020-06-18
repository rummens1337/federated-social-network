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
            alert("Login success")
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
        requestJSON('GET', window.location.origin + '/api/user/address?username=' + username, null, login, loginFailed);
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
