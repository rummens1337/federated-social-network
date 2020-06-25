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

        var data = new FormData(form)

        requestJSONFile('POST', dataServer + '/api/post/create', data, creationSucces, creationFailed);
      }

      // Central server needs to be set globally.
      requestJSON('GET', location.origin + '/api/user/address', null, create, null);
    }
  });
}

function create_comment(id) {
  $(`form[name='createcomment` + id + `']`).validate({
    rules: {
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
        requestJSON('POST', dataServer + '/api/post/comments/add', $(form).serialize(), creationSucces, creationFailed);
      }

      // Central server needs to be set globally.
      requestJSON('GET', location.origin + '/api/user/address', null, create, null);
    }
  });
}

// This function adds a post in the div 'posts_div'
function showPost(postdata, timeline=false) {
    var user = timeline ? postdata.username : null;
    var content = `<div class="media media-xs overflow-visible">
                    <a class="media-left" href="javascript:;"> <img id="image_post_` + postdata.post_id + `" src="/static/images/default.jpg" alt="" class="media-object img-circle"> </a>


                   <h5 style="color:black;">
                   <div class="media-body valign-middle" style="cursor: pointer;">
                   <b>`+ ((user != null) ? ('@' + user + '</b><br>') : "") + postdata.title + `</b></h5>
        </div></div>
        <h6 class="w3-text-black"><i class="fa fa-calendar fa-fw w3-margin-right"></i>` + postdata.creation_date + `</h6>
        <p class="w3-text-grey">` + postdata.body + `</p>`;


    if (postdata.image_url != '' && postdata.image_url != null) {
      var image = `<img style="width:80%" src=` + postdata.image_url +
                  `><br><p><a onclick="showComment(` + postdata.post_id + `)"> show comments</a><p>`;
    } else {
      var image = `<br><p><a onclick="showComment(` + postdata.post_id + `)"> show comments</a><p>`;
    }

        comments = `<div style="display:none;" class="comments" id='comments` + postdata.post_id + `'>
                 <form name="createcomment` + postdata.post_id + `">
                      <div class="input-group">
                            <textarea name="comment" id="comment" class="form-control" placeholder="Leave a comment below!" style="resize: none;"></textarea>
                            <input name="post_id" id="post_id" type="hidden" value="` + postdata.post_id + `">

                            <span class="input-group-addon">
                              <a href="#"><i class="fa fa-edit"></i></a>
                          </span>
                      </div>
                              <button class="submit" type="submit" onclick="create_comment(` + postdata.post_id + `);" >Comment</button>
                </form>
                      <ul class="comments-list" id=` + postdata.post_id + `>
                      </ul>
                    </div>`
        content = content + image + comments + `<hr>`;

    $('#posts_div').append(content);

    loadComments(postdata.post_id);

    if (postdata.profile_image != null) {
      document.getElementById('image_image_post_' + postdata.id).src = postdata.profile_image;
    }
}

function showComment(postid) {
  var x = document.getElementById("comments" + postid);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function loadComments(postid) {
  function getComments(req) {
    requestJSON("GET", req.data.address + "/api/post/comments", {"post_id": postid}, showcomments, commentsFailure);
  }

  function showcomments(req) {
    for (var i = 0; i < req.data.comments.length; i++) {
      loadComment(postid, req.data.comments[i]);
    }
  }

  function commentsFailure(req) {
    alertError(req.reason, 2000);
  }

  requestJSON("GET", "/api/user/address", null, getComments, null)
}

function loadComment(postid, comment) {
  var content = `<div class="p-10 bg-white">
                   <div class="media media-xs overflow-visible">
                      <a class="media-left" href="javascript:;"> <img id="image_comment_` + comment.id + `" src="/static/images/default.jpg" alt="" class="media-object img-circle"> </a>
                      <div class="media-body valign-middle" style="cursor: pointer;">
                        <b class="text-dark" onclick="location.href='../profile/` + comment.username + `';">` + comment.username + `</b><br>
                        <b class="text-inverse">` + comment.comment + `</b>
                      </div>
                      <div class="media-body valign-middle text-right overflow-visible">
                         <div class="btn-group dropdown">
                            <a href="javascript:;" class="btn btn-default">Options</a> <a href="javascript:;" data-toggle="dropdown" class="btn btn-default dropdown-toggle" aria-expanded="false"></a>
                         </div>
                      </div>
                   </div>
                </div>`;

  comment_list = document.getElementById(postid);
  comment_list.innerHTML += content;

  if (comment.profile_image != null) {
    document.getElementById('image_comment_' + comment.id).src = comment.profile_image;
  }
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
    $('#posts_div').append('<p class="w3-text-black">There are no posts on this profile &#128532.</p>\
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