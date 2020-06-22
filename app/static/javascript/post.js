// Global username used for retrieving posts.
// If not set. The user's own posts are loaded.
var username = null;

function create_post() {
  $("form[name='createpost']").validate({
    rules: {
      title: 'required',
      body: 'required'
    },

    submitHandler: function(form) {
      function creationSucces(req) {
        window.location.reload();
      }

      function creationFailed(response, XMLHttpRequest, textStatus, errorThrown) {
        alertError(response.reason, 2000);
      }

      function create(req) {
        dataServer = req.data.address;
        requestJSON('POST', dataServer + '/api/post/create', $(form).serialize(), creationSucces, creationFailed);
      }

      // Central server needs to be set globally.
      requestJSON('GET', location.origin + '/api/user/address', null, create, null);
    }
  });
}

// This function adds a post in the div 'posts_div'
function showPost(postdata, timeline=false) {
    var user = timeline ? postdata.username : null;
    var content = `<h5 style="color:#52B77C;"><b>`+ ((user != null) ? ('@' + user + '</b><br>') : "") + 
        postdata.title + `</b></h5>
        <h6 class="w3-text-teal"><i class="fa fa-calendar fa-fw w3-margin-right"></i>` + postdata.creation_date + `</h6>
        <p class="w3-text-grey">` + postdata.body + `</p>
        <hr>`;

    $('#posts_div').append(content);
}

// Call this function when requesting an array of posts, not implemented in backend yet but would greatly help.
function showPostsArray(req, timeline=false) {
  if (req.data.posts.length > 0) {
    for (i=0; i < req.data.posts.length; i++) {
        var post = req.data.posts[i];
        showPost(post, timeline);
    }
  }
  else {
    $('#posts_div').append('<p class="w3-text-grey">There are no posts on this profile &#128532.</p>\
                            <img src="/static/images/no-posts.jpg" width=100% alt="Y no posts bruh Q_Q">');
  }
}

function loadPosts(req) {
  var dataServer = req.data.address;
  var url = (username == null || username == "") ?
    dataServer + '/api/user/posts' :
    dataServer + '/api/user/posts?username=' + username;
  requestJSON('GET', url, null, showPostsArray, function(req) {
    alertError(req.reason, 2000)
  });
}

// Load the timeline
function loadTimeline(req) {
  var dataServer = req.data.address;
  var url = dataServer + '/api/user/timeline';
  requestJSON('GET', url, null, function(req) {
    showPostsArray(req, true);
  }, function(req) {
    alertError(req.reason, 2000)
  });
}

// Location can be 'posts' for a usernames own posts. Or 'timeline'
// for the users made timeline from its friends.
function loadUserPosts(u, location) {
  username = u;
  var url = (username == null || username == "") ?
    '/api/user/address' :
    '/api/user/address?username=' + username;

  if (location == 'posts') {
    requestJSON('GET', url, null, loadPosts, function(req) {
        alertError(req.reason, 2000)
    });
  } else if (location == 'timeline') {
    requestJSON('GET', url, null, loadTimeline, function(req) {
        alertError(req.reason, 2000)
    });
  }
}
