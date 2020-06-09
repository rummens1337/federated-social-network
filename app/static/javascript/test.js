$(function (){
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/user/',

        success: function(usernames) {
            alert(usernames)
            //$.each(usernames, function(i, us) {
            //    $usernames.append('<li>username: '+ us.usernames + '</li>');
            //});
        }
    });
});