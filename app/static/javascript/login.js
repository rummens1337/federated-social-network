$(function validateAccount() {
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
      $.ajax({
        data : $(form).serialize(),
        type : 'POST',
        url : 'http://localhost:9000/api/user/login',
        success : function(data) {
          alert("Succes");
        },
        error : function(data) {
          alert("Something went wrong")
        },
      })
    }
  });
});

$(function validatePassword() {
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
});