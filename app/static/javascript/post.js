function create_post() {
  $("form[name='createpost']").validate({
    rules: {
      title: 'required',
      body: 'required'
    },

    submitHandler: function(form) {
      function creationSucces(req) {
        alert("Post succesfully created!")
      }

      function creationFailed(XMLHttpRequest, textStatus, errorThrown) {
        alert("Failed to create post.")
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



$(document).ready( function() {

    function loadSucces(req) {
      showPostsArray(req);
      // alert("Post succesfully loaded!")
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
      alert(req.data.posts.length)
      for (i=0; i < req.data.posts.length; i++) {
        var post = req.data.posts[i];
        showPost(post);
      }
    }

    function loadFailed(XMLHttpRequest, textStatus, errorThrown) {
      alert("Something went wrong while retrieving posts.")
    }

    function loadPost(req) {
      dataServer = req.data.address;
      requestJSON('GET', dataServer + '/api/user/posts', null, loadSucces, loadFailed);
    }

    requestJSON('GET', location.origin + '/api/user/address', null, loadPost, loadFailed);
  }
);