$(function() {
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
      form.submit();
    }
  });
});

$(function validatePassword() {
  var validator = $("form[name='signup']").validate({
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
      form.submit();
    }
  });
});