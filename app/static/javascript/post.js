function create_post() {
  $("form[name='createpost']").validate({
    rules: {
      title: 'required',
      body: 'required'
    },

    submitHandler: function(form) {
      var username = "test";

      function getCookie() {
        var cookie = document.cookie.match('(^|;)\\s*access_token_cookie\\s*=\\s*([^;]+)')
        return cookie ? cookie.pop() : '';
      }

      function creationSucces(XMLHttpRequest, textStatus, errorThrown) {
        alert("Post succesfully created!")
      }

      function creationFailed(req) {
        alert("Failed to create post.")
      }

      function create(req) {
        dataServer = req.data.address;
        requestJSON('POST', dataServer + '/api/post/create', $(form).serialize(), creationSucces, creationFailed);
      }

      centralServer = "http://192.168.1.102:5000/"
      requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, create, null);
    }
  });
}



// $(document).ready( function() {
//     var username = "test";

//     function loadSucces(req) {
//       var json = JSON.parse(req);
//       alert("here");

//       var div = document.getElementById('posts_div')
//       var content = `<h5 style="color:#52B77C;"><b>`+ json['title'] + `</b></h5>
//         <h6 class="w3-text-teal"><i class="fa fa-calendar fa-fw w3-margin-right"></i>` + json['creation-date'] + `Just now</h6>
//         <p class="w3-text-grey">Im online</p>
//         <hr>`

//       $('#posts_div').append(content);

//       alert("Post succesfully created!")
//     }

//     function loadFailed(XMLHttpRequest, textStatus, errorThrown) {
//       alert("Something went wrong while retrieving posts.")
//     }

//     function loadPost(req) {
//       dataServer = req.data.address;
//       requestJSON('POST', dataServer + '/api/post/', , loadSucces, loadFailed);
//     }

//     centralServer = "http://192.168.1.102:5000/"
//     requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, loadPost, loadFailed);
//   }
// );