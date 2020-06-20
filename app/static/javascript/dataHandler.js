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
    var token = Cookies.get('access_token_cookie');
    var headers = {};
    if (token != null) headers = { 'Authorization' : 'Bearer ' + token };

    $.ajax({
        headers: headers,
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


function requestJSONFile(type, url, data=null, success=null, error=null) {
    var token = Cookies.get('access_token_cookie');
    var headers = {};
    if (token != null) headers = { 'Authorization' : 'Bearer ' + token };

    $.ajax({
        headers: headers,
        type: type,
        url: url,
        processData: false,
        contentType: false,
        data: data,
        crossDomain: true,
        success: function(req) {
            if (req.hasOwnProperty("data")) success(req);
            else error(req);
        },
        error: error
    });
};


/*
 * Shows an error message on screen.
 * Error   : type string, message to be shown.
 * ms      : type int,    amount of time to wait before closing error message
 * div_id  : type string, needs to be set if error message should be shown above a certain div
*/
function alertError(error, ms, div_id=null) {
    var dialog = document.createElement("div");

    dialog.innerHTML = error;
    dialog.setAttribute("class", "alert");
    dialog.setAttribute("id", "errorBox");

    if (div_id) {
        document.getElementById(div_id).appendChild(dialog);
    } else{
        document.body.appendChild(dialog);
    }


    setTimeout(function(){
    //   dialog.parentNode.removeChild(dialog);
      $('#errorBox').fadeOut(500);
    }, ms);
};

function handle_url_message() {
    let params = new URLSearchParams(window.location.search)

    if (params.has('message')) {
        let param = params.get('message');

        if (param == "registration_complete") {
            alertError("Registration Complete, you can now log in!", 2000);
        } else if (param == "registered") {
            alertError("Registered account, please check you email to verify it!", 4000);
        }
    }
}