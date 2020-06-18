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
            select_server: {
                "required": true
            }
        },
  
        submitHandler: function(form) {
          function editDataServer() {
            if (form.new_address.value == currentDataServer) {
                alertError("This data server is already registered to your account.", 2000);
            }
            else {
                serverForm = {new_address:form.select_server.value};
                requestJSON("GET", centralServer + "/api/user/edit", serverForm, editSucces, editFailed);
            }
          }
  
          function editSucces() {
            if(!alert('Your data server has been succesfully updated!')){window.location = "/settings/server";}
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
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, setNoDataAddress);

    function populateServerSelect(req) {
      var select = document.getElementById('select_server')
      var data = req.data.servers;
  
      for(i in data) {
        var server_option = document.createElement("option");
        server_option.value = data[i][1]
        server_option.textContent = data[i][0]
  
        select.appendChild(server_option);
      }
  
    }
  
    function requestError(req) {
      alert("Couldn't load servers...")
    }

    requestJSON("GET", centralServer + "/api/server", null, populateServerSelect, requestError);
});
