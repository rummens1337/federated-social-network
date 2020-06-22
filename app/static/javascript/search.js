function search_func() {
    $("form[name='search-form']").validate({
      rules: {
        search_input: "required",
      },

      submitHandler: function(form) {
        var input_data = $('input[id=search_input]');
        var data = '?username=' + input_data.val();

        function userFound(req) {
          users = req.data.users
          // TODO: populate the searchfield
          alertError(req.data.users, 2000)
        }

        function noUser(req) {
          alertError(req.reason, 2000)
        }

        // function search(req) {
        //   dataServer = req.data.address;
        //   requestJSON('GET', dataServer + '/api/search/search', $(form).serialize(), userFound, noUser);
        // }

        requestJSON('GET', '/api/user/search' + data, null, userFound, noUser);
      }
    });
}

function myFunction() {
  $(".dropdown-content").css({
    'min-width': ($(".dropdown").width() + 'px')
  });

  document.getElementById("search_dropdown").classList.toggle("show");
}

function filterContent() {
  var input, filter, a, i;

  input = document.getElementById("search_input");
  filter = input.value.toUpperCase();

  div = document.getElementById("search_dropdown");
  a = div.getElementsByTagName("a");

  for (i = 0; i < a.length; i++) {
    txtValue = a[i].innerText;

    if (txtValue.toUpperCase().indexOf(filter) != -1) {
      a[i].style.display = "";
    }
    else {
      a[i].style.display = "none";
    }
  }
}