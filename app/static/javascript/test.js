// GET or POST JSON from url and apply it to func.
// Params:
// - method: the method to use ('GET'/'POST').
// - url: the url to do the request to.
// - func: the function to apply the JSON data to.
function getJSON(method, url, func) {
    $.ajax({
        type: method,
        url: url,
        crossDomain: true,
        success: func(data)
    });
}

// Load usernames to recent friends list.
$( document ).ready(function (){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:9000/api/user/',
        crossDomain: true,

        success: function(json) {

            // Uncomment for debugging.
            // alert(json)
            
            // Get usernames div.
            var $usernames = $('#usernames');

            for (i in json.data.usernames) {
                $usernames.append('<li>username: '+ obj.data.usernames[i] + '</li>');
            }
        }
    });
});

// Load post_ids to recent posts list.
$( document ).ready(function (){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:9000/api/user/posts?username=user1',

        success: function(json) {

            // Uncomment for debugging.
            alert(json)
            
            // Get posts div.
            var $usernames = $('#usernames');

            for (i in json.data.posts) {
                $usernames.append('<li>username: '+ obj.data.usernames[i] + '</li>');
            }
        }
    });
});
