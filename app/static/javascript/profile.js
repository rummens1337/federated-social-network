var username = null;

function addFriend(friend) {
    requestJSON('GET', '/api/user/address', null, function(req) {
      requestJSON('POST', req.data.address + "/api/friend/add", {"friend" : friend }, function(req) {
        // Friend request is sent
        location.reload();
      }, function(req) {
        alertError(req.reason, 2000);
      });
    }, function(req) {
      alertError(req.reason, 2000);
    });
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

function acceptFriend(friend) {
    location.href = "/friend/requests";
}

// Set the HTML
// TODO
function profile(req) {
    var friend_status = req.data.friend;

    if (friend_status == 1) {
        document.getElementById('image_url').src = req.data.image_url;
        // document.getElementById('location').innerHTML = req.data.location;
        document.getElementById('name').innerHTML = req.data.firstname + ' ' + req.data.lastname;
        // document.getElementById('study').innerHTML = req.data.study;
        // document.getElementById('bio').innerHTML = req.data.bio;
    } else {
        document.getElementById('name').innerHTML = req.data.username;
        $("#stats").remove();
        $("#about").remove();
        $("#posts").remove();
    }
    
    if (document.getElementById('add_friend') != null) {
      var friend = req.data.username;
      if (friend_status == 0) document.getElementById('add_friend').innerHTML = "Befriend me!";
      else if (friend_status == 1) {
        document.getElementById('add_friend').innerHTML = "Unfriend";
        $("#add_friend").attr("onclick", "deleteFriend('"+friend+"')");
      }
      else if (friend_status == 2) {
        document.getElementById('add_friend').innerHTML = "Pending..";
        $("#add_friend").attr("onclick", "deleteFriend('"+friend+"')");
      }
      else if (friend_status == 3) {
        document.getElementById('add_friend').innerHTML = "Accept friendship request";
        $("#add_friend").attr("onclick", "acceptFriend('"+friend+"')");
      }
    }
}

// Get the data of the profile
function getProfile(req) {
    var dataServer = req.data.address;
    var url = (username == null || username == "") ?
      dataServer + '/api/user' :
      dataServer + '/api/user?username=' + username;
    requestJSON('GET', url, null, profile, function(req) {
      alertError(req.reason, 2000);
    });
}

// Get the address of the profile
function loadProfile(u) {
    username = u;
    setup();
    var url = (username == null || username == "") ?
      '/api/user/address' :
      '/api/user/address?username=' + username;
  
    requestJSON('GET', url, null, getProfile, function(req) {
      alertError(req.reason, 2000);
    });
}

// Setup the profile page
function setup() {
  if (getUsername() == username) {
    $("#add_friend").remove();
  }
}