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
        // Frontend/backend variabelen komen nog niet overeen
        data : $(form).serialize(),
        type : 'POST',
        url : '/api/user/register',
        success : function(){
          alert("Succesfully registered.")
        },
        error : function(data) {
          alert("Something went wrong")
        }
      })
    }
  });
}