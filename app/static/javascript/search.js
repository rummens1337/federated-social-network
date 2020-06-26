// Gets users from the central database based on what is typed in the search bar.
function search_func() {
  var input_data = $('input[id=search_input]');
  var data = '?username=' + input_data.val();

  function userFound(req) {
    var search_resp = document.getElementById('search_dropdown')
    search_resp.textContent = '';
    users = req.data.users

    for(var i = 0; i < users.length; i++) {

      var link = document.createElement('a');
      var username = users[i];
      var user_url = '/profile/' + username;

      link.innerHTML += username;
      link.href = user_url;

      search_resp.appendChild(link);
    }

  }

  function noUser(req) {
    alertError(req.reason, 2000)
  }

  requestJSON('GET', '/api/user/search' + data, null, userFound, noUser);
}

// Hides dropdown for search bar on click outside search bar.
$(document).click(function(e) {

  if ($("#search_dropdown").is(":visible") && !$(e.target).is('#search_input')) {
    document.getElementById("search_dropdown").classList.toggle("show");
  }
});

// Shows search bar if it's not already showing.
function showSearch() {
  $(".dropdown-content").css({
    'min-width': ($(".dropdown").width() + 'px')
  });

  if ($('#search_dropdown').is(":hidden")){
    document.getElementById("search_dropdown").classList.toggle("show");
  }
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