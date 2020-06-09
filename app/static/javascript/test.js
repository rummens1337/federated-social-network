$(function (){
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://95.217.178.90/api/user',

        success: function(usernames) {
            $.each(usernames, function(i, us) {
                $usernames.append('<li>username: '+ us.usernames + '</li>');
            });
        }
    });
});