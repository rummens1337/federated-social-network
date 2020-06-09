$(function (){
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/user/',

        success: function(usernames) {
            // alert(usernames)

            $usernames.append('<li>username: '+ usernames.usernames + '</li>');

        }
    });
});