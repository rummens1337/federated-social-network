// function search_func() {
//     $("form[name='search-form']").validate({
//       rules: {
//         search_input: "required",
//       },

//       submitHandler: function(form) {
//         var input_data = $('input[id=search_input]');
//         var data = 'username=' + input_data.val();
//         var username = 'test'

//         function userFound(XMLHttpRequest, textStatus, errorThrown) {
//           alert("User found in database!")
//         }

//         function noUser(req) {
//           alert("Failed to find user.")
//         }

//         function search(req) {
//           dataServer = req.data.address;
//           requestJSON('POST', dataServer + '/api/search/search', $(form).serialize(), userFound, noUser);
//         }

//         centralServer = "http://192.168.1.250:5000/"
//         requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, search, noUser);
//       }
//         // $.ajax({
//         //   // Frontend/backend variabelen komen nog niet overeen
//         //   data : data,
//         //   type : 'POST',
//         //   url : '/api/user/register',
//         //   error : function(data) {
//         //     alert("Something went wrong.")
//         //   }
//         // })
//     });
// }

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