$(function (){
    //var $usernames = $('#usernames');

    $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/user/',

        success: function(info) {
            alert(info)
            obj = JSON.parse(info)
            alert(obj.data.usernames)
            //for (var i in usernames.data.usernames) {
            //    alert(i)
            //}

            //$( 'li' ).each(usernames, function(i, us) {
            //    $usernames.append('<li>username: '+ us.usernames + '</li>');
            //});
            alert('done')
        }
    });
});