function validateAccount() {
  $("form[name='login']").validate({
    rules: {
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
      }
    },
    messages: {
      email: "Please enter a valid email address",

      password: {
        required: "Please enter password",
      }

    },

    submitHandler: function(form) {
      // TODO: dummy username
      var username = "test";

      function loginFailed(XMLHttpRequest, textStatus, errorThrown) {
        alert("Login failed")
      }

      function loginSuccess(req) {
        alert("Login success")
      }

      function login(req) {
        dataServer = req.data.address;
        requestJSON('POST', dataServer + '/api/user/login', $(form).serialize(), loginSuccess, loginFailed);
      }
      
      centralServer = "http://192.168.1.250:5000/"
      requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, login, loginFailed);
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