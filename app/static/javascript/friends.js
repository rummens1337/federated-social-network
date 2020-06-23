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
  // var content = '<a href="/profile/'+ friend.username + '"> \
  //   <li class="friend selected"><img src="/static/images/default.jpg"><div class="name">' +
  //   friend.username + '</div></li></a>';
  var content = `<div class="p-10 bg-white">
                   <div class="media media-xs overflow-visible">
                      <a class="media-left" href="javascript:;"> <img src="/static/images/default.jpg" alt="" class="media-object img-circle"> </a>
                      <div class="media-body valign-middle" onclick="location.href='/profile/`+friend.username+`';" style="cursor: pointer;">
                        <b class="text-dark">` + friend.username + `</b><br>
                        <b class="text-inverse">` + friend.username + `</b>
                      </div>
                      <div class="media-body valign-middle text-right overflow-visible">
                         <div class="btn-group dropdown">
                            <a href="javascript:;" class="btn btn-default">Friends</a> <a href="javascript:;" data-toggle="dropdown" class="btn btn-default dropdown-toggle" aria-expanded="false"></a>
                            <ul class="dropdown-menu dropdown-menu-right" x-placement="bottom-end" style="position: absolute; will-change: transform; top: 0px; left: 0px; transform: translate3d(101px, 34px, 0px);">
                               <li><a href="javascript:deleteFriend('` + friend.username +`');;">Delete</a></li>
                               <li><a href="javascript:;">Action 2</a></li>
                               <li><a href="javascript:;">Action 3</a></li>
                               <li class="divider"></li>
                               <li><a href="javascript:;">Action 4</a></li>
                            </ul>
                         </div>
                      </div>
                   </div>
                </div>`;
  $('#friend-list').append(content);
}

function deleteFriend(friend) {
    requestJSON('GET', '/api/user/address', null, function(req) {
        requestJSON('POST', req.data.address + "/api/friend/delete", {"friend" : friend }, function(req) {
            // Friend is deleted
            location.reload();
        }, function(req) {
            alertError('hello there', 2000);
        });
    }, function(req) {
        alertError('general kenobi', 2000);
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
