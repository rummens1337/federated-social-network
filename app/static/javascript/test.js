// URL of servers ENDING WITH /
var centralServer = 'http://localhost:5000/'
var dataServer = 'http://localhost:9000/';

// User variables.
var username = 'user1';

// GET or POST JSON from url and apply it to func.
// Params:
// - type: the request type to use ('GET'/'POST').
// - url: the url to do the request to.
// - func: the function to apply the JSON data to.
function requestJSON(type, url, func) {

    $.ajax({
        type: type,
        url: url,
        crossDomain: true,
        success: func
    });
}

// DIT WERKT NOG NIET
// Get address of data server for this user from the central server.
//var getDataServer = function(req) {
//    dataServer = req.data.address;
//}
//$(document).ready(requestJSON('GET', centralServer + 'api/user/', getDataServer));

var applyUsernames = function(req) {
    // Get usernames div.
    var $usernames = $('#usernames');

    for (i in req.data.usernames) {
        $usernames.append('<li>username: '+ req.data.usernames[i] + '</li>');
    }
}
$(document).ready(requestJSON('GET', dataServer + 'api/user/', applyUsernames));

var applyPosts = function(req) {
    // Get posts div.
    var $usernames = $('#posts');

    for (i in req.data.posts) {
        $usernames.append('<li>POST: '+ req.data.posts[i] + '</li>');
    }
}
$(document).ready(requestJSON('GET', dataServer + 'api/user/posts?username=' + username, applyPosts));
