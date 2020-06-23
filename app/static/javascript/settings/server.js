var currentDataServer = "";
var centralServer = window.location.origin;

function setDataAddress(req) {
    currentDataServer = req.data.address;
    document.getElementById('dataserveraddress').innerHTML = '<b>Server address: </b>' + currentDataServer;
    document.getElementById('dataservername').innerHTML = '<b>Server name: </b>' + req.data.name;
}

function setNoDataAddress() {
    document.getElementById('dataservername').innerHTML = "no server registered";
    document.getElementById('dataserveraddress').classList.add("w3-hide");
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
            if (form.select_server.value == currentDataServer) {
                alertError("This data server is already registered to your account.", 2000);
            }
            else {
                serverForm = {new_address:form.select_server.value};
                requestJSON("POST", "/api/user/edit", serverForm, editSucces, editFailed);
            }
          }
  
          function editSucces() {
            if(!alertError('Your data server has been succesfully updated!', 2000)){
                requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, setNoDataAddress);
            }
          }
  
          function editFailed(response) {
            console.log(response)
            alertError(response.reason, 2000);
          }
          
          editDataServer();
        }
    });
}

function exportData() {
    $("form[name='exportdata']").validate({
        rules: {
        },
  
        submitHandler: function(form) {
          function exportDataServer() {
            requestJSONMigrationFile("GET", currentDataServer + "/api/user/export", null, exportSucces, exportFailed);
          }
  
          function exportSucces(res) {
            console.log(res)
            var blob = new Blob([res], {type: "application/zip"});
            saveAs(blob, "export.zip")
            alertError("Exporting data, please do not leave this page until this process has finished!", 5000);
          }
  
          function exportFailed(response) {
            console.log(response)
            alertError(response.reason, 2000);
          }
          
          exportDataServer();
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
