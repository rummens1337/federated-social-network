// URL of data server ENDING WITH /
var dataServer = 'http://localhost:9000/';

// GET or POST JSON from url and apply it to func.
// Params:
// - type: the request type to use ('GET'/'POST').
// - api: the api on the data server to do the request to.
// - func: the function to apply the JSON data to.
function requestJSON(type, api, func) {
    url = dataServer + api;

    $.ajax({
        type: type,
        url: url,
        crossDomain: true,
        success: func
    });
}

var applyUsernames = function(json) {    
    // Get usernames div.
    var $usernames = $('#usernames');

    for (i in json.data.usernames) {
        $usernames.append('<li>username: '+ json.data.usernames[i] + '</li>');
    }
}
$(document).ready(requestJSON('GET', 'api/user/', applyUsernames));

var applyPosts = function(json) {
    // Get posts div.
    var $usernames = $('#posts');
    alert(json)
    for (i in json.data.posts) {
        $usernames.append('<li>POST: '+ json.data.posts[i] + '</li>');
    }
}
$(document).ready(requestJSON('GET', 'api/user/posts?username=user1', applyPosts));
