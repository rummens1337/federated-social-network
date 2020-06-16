var currentDataServer = "";
var centralServer = "http://172.19.0.1:5000/";

username="testuser"

function setDataAddress(req) {
    currentDataServer = req.data.address;
    document.getElementById('dataserveraddress').innerHTML = currentDataServer;
}

$(document).ready(function() {
    requestJSON('GET', centralServer + 'api/user/address?username=' + username, null, setDataAddress, null);
});