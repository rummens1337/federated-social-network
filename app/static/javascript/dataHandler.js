// URL of servers ENDING WITH '/'
// centralServer is hardcoded
// dataServer is requested using function getDataServer
// var centralServer = 'http://localhost:5000/'
// var dataServer = 'http://localhost:9000/';

// GET or POST JSON from url and apply it to func.
// Params:
// - type: the request type to use ('GET'/'POST').
// - url: the url to do the request to.
// - func: the function to apply the JSON data to.
function requestJSON(type, url, data=null, success=null, error=null) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        crossDomain: true,
        success: function(req) {
            if (req.hasOwnProperty("data")) success(req);
            else error(req);
        },
        error: error
    });
};