var currentDataServer = "";
var centralServer = window.location.origin;

function setDataAddress(req) {
    currentDataServer = req.data.address;
    document.getElementById('dataserveraddress').innerHTML = currentDataServer;
}

function setNoDataAddress() {
    document.getElementById('dataserveraddress').innerHTML = "no server registered";
    document.getElementById('dataserveraddress').style.color = "red";
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, setNoDataAddress);
});