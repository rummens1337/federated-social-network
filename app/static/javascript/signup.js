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
        $.ajax({
          data : $(form).serialize(),
          type : 'POST',
          url : '/api/user/register',
          success : function(data) {
            alert("succes");
          },
          error : function(data) {
            alert("no")
          }
        })
      }
    });
  }


// function sign_up() {
//     alert('..')
// }