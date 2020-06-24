// Call this function when requesting an array of friends
function showFriends(req) {
  if (req.data.friends.length > 0) {
    for (i=0; i < req.data.friends.length; i++) {
        var friend = req.data.friends[i];
        show(friend);
        // alert(friend);
        // console.log(friend);

        loadProfile(friend.username);
    }
  }
  else {
    // TODO: make work with the template tean frontend!
    $('#friend-list').append('<p class="w3-text-grey">There are no friends to show...</p>');
  }
}

// Get the address of the profile
function loadProfile(u) {
    username = u;
    var url = (username == null || username == "") ?
      '/api/user/address' :
      '/api/user/address?username=' + username;
    requestJSON('GET', url, null, getProfile, function(req) {
      alertError(req.reason, 2000);
      location.href = "/";
    });
}

// Get the data of the profile
function getProfile(req) {
    var dataServer = req.data.address;
    var urlProfile = dataServer + '/api/user?username=' + req.data.username
    requestJSON('GET', urlProfile, null, profile, function(req) {
        alertError(req.reason, 2000);
        location.href = "/";
    });
}

function profile(req) {
  // alert(req.data.username);
    // document.getElementById('image_url').src = req.data.image_url;
    document.getElementById('image_url_' + req.data.username).innerHTML = '<img src="' + req.data.image_url + '" alt="" class="media-object img-circle">';
    document.getElementById('full_name_' + req.data.username).innerHTML = req.data.firstname + ' ' + req.data.lastname;
}

// This function adds a friend in the div 'friend'
function show(friend) {
  var content = `<div class="p-10 bg-white">
                   <div class="media media-xs overflow-visible">
                      <a class="media-left" id="image_url_` + friend.username + `" href="javascript:;">  </a>
                      <div class="media-body valign-middle" onclick="location.href='/profile/`+friend.username+`';" style="cursor: pointer;">
                        <b id="full_name_` + friend.username + `" class="text-dark">USERNAME</b><br>
                        <b class="text-inverse">` + friend.username + `</b>
                      </div>
                      <div class="media-body valign-middle text-right overflow-visible">
                         <div class="btn-group dropdown">
                            <a href="javascript:;" class="btn btn-default">Options</a> <a href="javascript:;" data-toggle="dropdown" class="btn btn-default dropdown-toggle" aria-expanded="false"></a>
                            <ul class="dropdown-menu dropdown-menu-right" x-placement="bottom-end" style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(101px, 34px, 0px);">
                               <li><a href="javascript:deleteFriend('` + friend.username +`');;">Unfriend</a></li>
                            </ul>
                         </div>
                      </div>
                   </div>
                </div>`;
  $('#friend-list').append(content);
  // loadProfile(friend.username);
}

function deleteFriend(friend) {
    requestJSON('GET', '/api/user/address', null, function(req) {
        requestJSON('POST', req.data.address + "/api/friend/delete", {"friend" : friend }, function(req) {
            // Friend is deleted
            location.reload();
        }, function(req) {
            alertError(req.reason, 2000);
        });
    }, function(req) {
        alertError(req.reason, 2000);
    });
}

function setDataAddress(req) {
  dataServer = req.data.address;
  requestJSON('GET', dataServer + '/api/friend/all', null, showFriends, function(req) {
    alertError(req.reason, 2000);
  });
}

$(document).ready(function() {
  requestJSON('GET', '/api/user/address', null, setDataAddress, function(req) {
    alertError(req.reason, 2000);
  });
});
