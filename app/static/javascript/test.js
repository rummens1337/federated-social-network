var applyUsernames = function(req) {
    // Get usernames div.
    var $usernames = $('#usernames');
    for (i in req.data.usernames) {
        $usernames.append('<li>username: '+ req.data.usernames[i] + '</li>');
    }
};

var applyPosts = function(req) {
    // Get posts div.
    var $posts = $('#posts');

    for (i in req.data.posts) {
        $posts.append('<div>POST: '+ req.data.posts[i] + '</div>');
    }
};

$(document).ready(function() {
    if (dataServer == '') {
        // Set dataserver for development.
        dataServer = 'http://localhost:9000/'
    }
    else {
        requestJSON('GET', dataServer + 'api/user/', applyUsernames);
        requestJSON('GET', dataServer + 'api/user/posts?username=' + username, applyPosts);
    }
});

