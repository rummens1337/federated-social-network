// Call this function when requesting an array of friends
function showFriends(req) {
  if (req.data.friends.length > 0) {
    for (i=0; i < req.data.friends.length; i++) {
        var friend = req.data.friends[i];
        show(friend);
    }
  }
  else {
    // TODO: make work with the template tean frontend!
    $('#friend-list').append('<p class="w3-text-grey">There are no friends to show...</p>');
  }
}

// This function adds a friend in the div 'friend'
function show(friend) {
  var content = '<a href="/profile/'+ friend.username + '"> \
    <li class="friend selected"><img src="/static/images/default.jpg"><div class="name">' + 
    friend.username + '</div></li></a>';
  $('#friend-list').append(content);
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
