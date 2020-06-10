// Load usernames to recent friends list.
$( document ).ready(function (){
    // Get usernames div.
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:9000/api/user/',
        crossDomain: true,

        success: function(json) {

            // Uncomment for debugging.
            // alert(json)

            for (i in json.data.usernames) {
                $usernames.append('<li>username: '+ obj.data.usernames[i] + '</li>');
            }
        }
    });
});

// Load post_ids to recent posts list.
$( document ).ready(function (){
    // Get posts div.
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:9000/api/user/posts?username=user1',

        success: function(json) {

            // Uncomment for debugging.
            alert(json)

            for (i in json.data.posts) {
                $usernames.append('<li>username: '+ obj.data.usernames[i] + '</li>');
            }
        }
    });
});
