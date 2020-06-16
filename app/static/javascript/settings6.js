$(function saveProfile() {
    $("form[name='settings']").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            firstname: 'required',
            username: 'required',
        },

        messages: {
            email: "Please enter a valid email address"
        },

        submitHandler: function(form) {
            $.ajax({
                data : $(form).serialize(),
                type : 'POST',
                url : 'http://localhost:9000/api/user/details',
                success : function(data) {
                    alert("Succes");
                },
                error : function(data) {
                    alert("Something went wrong")
                },
            })
        }
    });
});
