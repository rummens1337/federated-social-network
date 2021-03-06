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

function exportData() {
    function exportSucces(res) {
        var blob = new Blob([res], {type: "application/zip"});
        saveAs(blob, "export.zip");
    }

    function exportFail() {
        alertError("Exporting is not possible at this moment. Please try again at another time.", 10000);
    }

    alertError("Exporting data from server. Please leave this page open until this process has finished.", 5000);
    requestJSONMigrationFile("GET", currentDataServer + "/api/user/export", null, exportSucces, exportFail);
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
                // Step 1: Export data from old server.
                alertError("Step 1/4: Exporting data from old server. Please leave this page open until this process has finished.", 5000);
                requestJSONMigrationFile("GET", currentDataServer + "/api/user/export", null, exportSucces, migrationFailed);
            }
          }

          function exportSucces(res) {
            var blob = new Blob([res], {type: "application/zip"});

            if (form.save_data_zip.checked == true) {
                saveAs(blob, "export.zip");
            }

            // Step 2: Import data in new server.
            var data = new FormData()
            data.append('new_address', form.select_server.value);
            data.append('file', blob, "import.zip");

            console.log("Export success.");
            alertError("Step 2/4: Importing data to new server. Please leave this page open until this process has finished.", 5000)
            requestJSONFile("POST", form.select_server.value + "/api/user/import", data, importSucces, migrationFailed);
          }

          function editFailed(res) {
            // Step 3 failed.
            console.log("Edit central server failed. Reason: " + res.reason);
            alertError("Migration failed in step 3: the central server registration failed to update, please contact support!", 20000);
          }

          function importSucces(res) {
            // Step 3 Update address in central server.
            serverForm = {new_address:form.select_server.value};
            console.log("Imported " + res.data.filename + "on new server.");
            alertError("Step 3/4: Editing central server registration for your account. Please leave this page open until this process has finished.", 5000);
            requestJSON("POST", "/api/user/edit", serverForm, editSuccess, editFailed);
          }

          function deleteFailed(res) {
            // Step 4 failed.
            console.log("Delete failed. Reason: " + res.reason);
            alertError("Migration success! But your data could not be deleted from your old data server. Please contact the owner of your old data server! However, you can use FedNet on the new data server." , 20000);
          }

          function editSuccess(res) {
            // Step 4: Delete data from old server.
            console.log("Editing entry in central server success.")
            alertError("Step 4/4: Deleting data from old data server. Please leave this page open until this process has finished.", 5000);
            requestJSON("POST", currentDataServer + "/api/user/delete", null, deleteFromOldServerSuccess, deleteFailed);
          }

          function deleteFromOldServerSuccess(res) {
            // Step 5: Set info on settings page.
            console.log("Delete success. Migrate completed.")
            setDataAddress({data:{address:form.select_server.value, name:form.select_server.textContent}});
            alertError("Migration success! Your new server will appear on the top of this page.", 10000)
          }
  
          function migrationFailed(response) {
            console.log(response)
            alertError("A problem occurred during the migration process. You can still use FedNet using your old data server!", 10000);
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
