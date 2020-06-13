// URL of servers ENDING WITH '/'
// centralServer is hardcoded
// dataServer is requested using function getDataServer
var centralServer = 'http://localhost:5000/'
var dataServer = 'http://localhost:9000/';

// User variables.
var username = 'testuser';

// GET or POST JSON from url and apply it to func.
// Params:
// - type: the request type to use ('GET'/'POST').
// - url: the url to do the request to.
// - func: the function to apply the JSON data to.
function requestJSON(type, url, func) {
    $.ajax({
        type: type,
        url: url,
        crossDomain: true,
        success: func
    });
};

// Get address of data server for this user from the central server.
var getDataServer = function(req) {
    dataServer = req.data.address;
};

$(document).ready(function() {
    requestJSON('GET', centralServer + 'api/user/address?username=' + username, getDataServer);
});