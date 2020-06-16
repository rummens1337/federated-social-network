var currentDataServer = "";
var centralServer = "0.0.0.0:5000";

username="testuser"

// Get address of data server for this user from the central server.
var getDataServer = function(req) {
    alert(req.data.address)
    currentDataServer = req.data.address;
    alert(currentDataServer)
};

function setDataAddress() {
    $('#dataserveraddress').innerHTML = currentDataServgiter;
}

$(document).ready(function() {
    requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, getDataServer, null);
    setDataAddress();
});