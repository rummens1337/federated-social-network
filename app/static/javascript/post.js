function create_post() {
    $("form[name='createpost']").validate({
      rules: {
        title: 'required',
        body: 'required'
      },

      submitHandler: function(form) {
        var data = new FormData($(this));

        $.ajax({
          data : FormData,
          // Gebruiken wanneer Frontend en backend dezelfde variabelen gebruiken.
          // data : $(form).serialize(),
          type : 'POST',
          url : 'http://localhost:9000/api/post/create',
          success : function(data) {
            alert("Succes");
          },
          error : function(data) {
            alert("Something went wrong while trying to post.")
          },
          cache : false
        })
      }
    });
  }