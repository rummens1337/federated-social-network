function search_func() {
    $("form[name='search-form']").validate({
      rules: {
        search_input: "required",
      },
      submitHandler: function(form) {
        var input_data = $('input[name=search_input]');
        var data = 'username=' + input_data.val();

        $.ajax({
          // Frontend/backend variabelen komen nog niet overeen
          data : data,
          type : 'POST',
          url : '/api/user/register',
          error : function(data) {
            alert("Something went wrong.")
          }
        })
      }
    });
  }