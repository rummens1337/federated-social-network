function search_func() {
    $("form[name='search-form']").validate({
      rules: {
        search_input: "required",
      },

      submitHandler: function(form) {
        var input_data = $('input[id=search_input]');
        var data = 'username=' + input_data.val();
        var username = 'test'

        function userFound(XMLHttpRequest, textStatus, errorThrown) {
          alert("User found in database!")
        }

        function noUser(req) {
          alert("Failed to find user.")
        }

        function search(req) {
          dataServer = req.data.address;
          requestJSON('POST', dataServer + '/api/search/search', $(form).serialize(), userFound, noUser);
        }

        centralServer = "http://192.168.1.250:5000/"
        requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, search, noUser);
      }
        // $.ajax({
        //   // Frontend/backend variabelen komen nog niet overeen
        //   data : data,
        //   type : 'POST',
        //   url : '/api/user/register',
        //   error : function(data) {
        //     alert("Something went wrong.")
        //   }
        // })
    });
}