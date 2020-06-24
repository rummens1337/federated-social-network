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

function migrateData() {
    $("form[name='migratedata']").validate({
        rules: {
            select_server: {
                "required": true
            }
        },
  
        submitHandler: function(form) {
          function exportDataServer() {
            if (form.select_server.value == currentDataServer) {
                alertError("This data server is already registered to your account.", 2000);
            }
            else {
                serverForm = {new_address:form.select_server.value};
                requestJSONMigrationFile("GET", currentDataServer + "/api/user/export", null, exportSucces, migrationFailed);
            }
          }

          function importSucces(res) {
            setDataAddress({data:{address:form.select_server.value, name:form.select_server.textContent}});
            alertError("Importing success, your new server will appear on the top of this page. Filename: " + res.data.filename, 5000)
          }
  
          function exportSucces(res) {
            alertError("Exporting data, please do not leave this page until this process has finished!", 5000);
            var blob = new Blob([res], {type: "application/zip"});

            // Use this to download file to browser (maybe option).
            // saveAs(blob, "export.zip")

            // To set to user chosen new server.
            var newServer = currentDataServer;

            var data = new FormData()
            data.append('new_address', form.select_server.value);
            data.append('file', blob, "import.zip");

            requestJSONFile("POST", newServer + "/api/user/import", data, importSucces, migrationFailed);
          }
  
          function migrationFailed(response) {
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
