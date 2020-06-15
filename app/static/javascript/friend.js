function add_friend() {
    $("form[name='addFriend']").validate({

      submitHandler: function(form) {

        $.ajax({
          data : FormData,
          // Gebruiken wanneer Frontend en backend dezelfde variabelen gebruiken.
          // data : $(form).serialize(),
          type : 'POST',
          url : 'http://localhost:9000/api/friend/register',
          success : function(data) {
            alert("Succes");
          },
          error : function(data) {
            alert("Something went wrong while trying to post.")
          }
        })
      }
    });
  }