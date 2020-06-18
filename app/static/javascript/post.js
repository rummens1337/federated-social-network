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
        if(!alert('Post succesfully created!')){window.location.reload();}
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

function loadSucces(req) {
  showPostsArray(req);
}

// This function adds a post in the div 'posts_div'
function showPost(postdata) {
  var div = document.getElementById('posts_div')
  var content = `<h5 style="color:#52B77C;"><b>`+ postdata.title + `</b></h5>
    <h6 class="w3-text-teal"><i class="fa fa-calendar fa-fw w3-margin-right"></i>` + postdata.creation_date + `</h6>
    <p class="w3-text-grey">` + postdata.body + `</p>
    <hr>`

  $('#posts_div').append(content);

}

// Call this function when requesting an array of posts, not implemented in backend yet but would greatly help.
function showPostsArray(req) {
  for (i=0; i < req.data.posts.length; i++) {
    var post = req.data.posts[i];
    showPost(post);
  }
}

function loadFailed(req, XMLHttpRequest, textStatus, errorThrown) {
  alertError(req.reason, 2000)
}

function loadPosts(req) {
  var dataServer = req.data.address;
  var url = (username == null || username == "") ?
    dataServer + '/api/user/posts' :
    dataServer + '/api/user/posts?username=' + username;
  requestJSON('GET', url, null, loadSucces, loadFailed);
}

// Load the timeline
function loadTimeline(req) {
  var dataServer = req.data.address;
  var url = dataServer + '/api/user/timeline';
  requestJSON('GET', url, null, loadSucces, loadFailed);
}

// Location can be 'posts' for a usernames own posts. Or 'timeline'
// for the users made timeline from its friends.
function loadUserPosts(u, location) {
  username = u;
  var url = (username == null || username == "") ?
    '/api/user/address' :
    '/api/user/address?username=' + username;

  if (location == 'posts') {
    requestJSON('GET', url, null, loadPosts, loadFailed);
  } else if (location == 'timeline') {
    requestJSON('GET', url, null, loadTimeline, loadFailed);
  }
}
