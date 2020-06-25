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

function create_comment() {
  $("form[name='createcomment']").validate({
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
        requestJSON('POST', dataServer + '/api/post/addComment', $(form).serialize(), creationSucces, creationFailed);
      }

      // Central server needs to be set globally.
      requestJSON('GET', location.origin + '/api/user/address', null, create, null);
    }
  });
}

// This function adds a post in the div 'posts_div'
function showPost(postdata, timeline=false) {
    var user = timeline ? postdata.username : null;
    var content = `<h5 style="color:#52B77C;">
                    <b>`+ ((user != null) ? ('@' + user + '</b><br>') : "") + postdata.title + `</b></h5>
        <h6 class="w3-text-teal"><i class="fa fa-calendar fa-fw w3-margin-right"></i>` + postdata.creation_date + `</h6>
        <p class="w3-text-grey">` + postdata.body + `</p>
        <a onclick="showComment(` + postdata.post_id + `)"> show comments</a>`;
        comments = `<div style="display:none;" class="comments"  id='comments` + postdata.post_id + `'>
                 <form name="createcomment">
                      <div class="input-group">

                            <textarea name="comment" id="comment" class="form-control" placeholder="Leave a comment below!" style="resize: none;"></textarea>
                            <input name="post_id" id="post_id" type="hidden" value= ` + postdata.post_id + `>

                            <span class="input-group-addon">
                              <a href="#"><i class="fa fa-edit"></i></a>
                          </span>
                      </div>
                              <button class="submit" type="submit" onclick="create_comment();" >Comment</button>
                </form>
                      <ul class="comments-list">
                        ` + loadComments(postdata.post_id) +`
                      </ul>
                    </div>`
        content = content + comments + `<hr>`;

    $('#posts_div').append(content);
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
  comment = {
            'id': 5,
            'comment': 'hello there',
            'username': 'bas',
            'creation_date': 'nu',
            'last_edit_date': 'toen'
        };
  return loadComment(postid, comment);
}

function loadComment(postid, comment) {
  var style = `<style>
                .media.media-xs .media-object {
                    width: 64px;
                }
                .m-b-2 {
                    margin-bottom: 2px!important;
                }
                .media>.media-left, .media>.pull-left {
                    padding-right: 15px;
                }
                .media-body, .media-left, .media-right {
                    display: table-cell;
                    vertical-align: top;
                }
              </style>`
  var content = `<div class="p-10 bg-white">
                   <div class="media media-xs overflow-visible">
                      <a class="media-left" href="javascript:;"> <img src="/static/images/default.jpg" alt="" class="media-object img-circle"> </a>
                      <div class="media-body valign-middle" style="cursor: pointer;">
                        <b class="text-dark" onclick="location.href='../profile/` + comment.username + `';">` + comment.username + `</b><br>
                        <b class="text-inverse">` + comment.comment + `</b>
                      </div>
                      <div class="media-body valign-middle text-right overflow-visible">
                         <div class="btn-group dropdown">
                            <a href="javascript:;" class="btn btn-default">Options</a> <a href="javascript:;" data-toggle="dropdown" class="btn btn-default dropdown-toggle" aria-expanded="false"></a>
                            <ul class="dropdown-menu dropdown-menu-right" x-placement="bottom-end" style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(101px, 34px, 0px);">
                               <li><a href="javascript:;">Delete</a></li>
                               <li><a href="javascript:;">Edit</a></li>
                            </ul>
                         </div>
                      </div>
                   </div>
                </div>`;
  return style + content;
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