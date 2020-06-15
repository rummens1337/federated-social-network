function changeTab(evt, tabtoggle) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the link that opened the tab
  document.getElementById(tabtoggle).style.display = "block";
  evt.currentTarget.className += " active";
}



var applyUsernames = function(req) {
    // Get usernames div.
    var $usernames = $('#usernames');
    for (i in req.data.usernames) {
        $usernames.append('<li>username: '+ req.data.usernames[i] + '</li>');
    }
};

var applyPosts = function(req) {
    // Get posts div.
    var $posts = $('#posts');

    for (i in req.data.posts) {
        $posts.append('<div>POST: '+ req.data.posts[i] + '</div>');
    }
};

$(document).ready(function() {
    if (dataServer == '') {
        // Set dataserver for development.
        dataServer = 'http://localhost:9000/'
    }
    else {
        requestJSON('GET', dataServer + 'api/user/', applyUsernames);
        requestJSON('GET', dataServer + 'api/user/posts?username=' + username, applyPosts);
    }
});

