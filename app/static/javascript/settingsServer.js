var currentDataServer = "";
var centralServer = window.location.origin;

function setDataAddress(req) {
    currentDataServer = req.data.address;
    document.getElementById('dataserveraddress').innerHTML = currentDataServer;
    document.getElementById('dataserveraddress').style.color = "lime";
}

function setNoDataAddress() {
    document.getElementById('dataserveraddress').innerHTML = "no server registered";
    document.getElementById('dataserveraddress').style.color = "red";
}

function updateDataServer() {
    $("form[name='editdataserver']").validate({
        rules: {
            new_address: {
                "required": true,
                startsWithHTTP: true,
                endsWithSlash: true
            }
        },
  
        submitHandler: function(form) {
          function editDataServer() {
            if (form.new_address.value == currentDataServer) {
                alertError("This data server is already registered to your account.", 2000);
            }
            else {
                serverForm = {new_address:form.new_address.value};
                requestJSON("GET", centralServer + "/api/user/edit", serverForm, editSucces, editFailed);
            }
          }
  
          function editSucces() {
            if(!alert('Your data server has been succesfully registered!')){window.location = "/settings/server";}
          }
  
          function editFailed(response) {
            console.log(response)
            alertError(response.reason, 2000);
          }
          
          editDataServer();
        }
    });
}

$(document).ready(function() {
    jQuery.validator.addMethod("startsWithHTTP", function(value, element) {
        return value.startsWith('http://');
    }, "Server address should start with http://");

    jQuery.validator.addMethod("endsWithSlash", function(value, element) {
        return !value.endsWith('/');
    }, "Server address may not end with /");

    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, setNoDataAddress);
});
