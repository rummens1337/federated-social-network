$(function signup() {
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
        //form.submit();
      }
    });
  });

function signup() {
    alert('..')
}