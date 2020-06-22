var dataServer = null;

// Call this function when requesting an array of requests
function showRequests(req) {
    if (req.data.friends.length > 0) {
        for (i=0; i < req.data.friends.length; i++) {
            var friend = req.data.friends[i];
            show(friend);
        }
    }
    else {
        // TODO: make work with the template team frontend!
        $('#request-list').append('<p class="w3-text-grey">There are no requests to show...</p>');
    }
}

function accept(id, accept) {
    var data = {'id' : id, 'accept' : accept}
    requestJSON('POST', dataServer + '/api/friend/accept', data, function(req) {
        location.reload();
        return false;
    }, function(req) {
        alertError(req.reason, 2000);
    });
}
  
// This function adds a friend in the div 'friend'
function show(friend) {
    var content = friend.username + 
        '<button onclick="accept('+friend.id+', 1)">accept</button> \
        <button onclick="accept('+friend.id+', 0)">decline</button><br>';
    $('#request-list').append(content);
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/friend/requests', null, showRequests, function(req) {
        alertError(req.reason, 2000);
    });
}

$(document).ready(function() {
    requestJSON('GET', '/api/user/address', null, setDataAddress, function(req) {
        alertError(req.reason, 2000);
    });
});
