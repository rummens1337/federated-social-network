var centralServer = window.location.origin;

function setUserSettings(req) {
    document.getElementById('image_url').src = req.data.image_url;
    document.getElementById('location').innerHTML = req.data.location;
    document.getElementById('name').innerHTML = req.data.firstname + ' ' + req.data.lastname;
    document.getElementById('study').innerHTML = req.data.study;
    document.getElementById('bio').innerHTML = req.data.bio;
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/user', null, setUserSettings, null);
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, null);
});
