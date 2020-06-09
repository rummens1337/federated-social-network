$(function (){
    var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/user/',

        success: function(info) {
            // alert(usernames)
            obj = JSON.parse(info)

            for (i in obj.data.usernames) {
                $usernames.append('<li>username: '+ obj.data.usernames[i] + '</li>');
            }
        }
    });
});