var username = null;

function error(req) { 
    // TODO: use our custom error 
    alert("Error during loading.");
}

// Set the HTML
// TODO
function profile(req) {
    document.getElementById('image_url').src = req.data.image_url;
    // document.getElementById('location').innerHTML = req.data.location;
    document.getElementById('name').innerHTML = req.data.firstname + ' ' + req.data.lastname;
    // document.getElementById('study').innerHTML = req.data.study;
    // document.getElementById('bio').innerHTML = req.data.bio;
}

// Get the data of the profile
function getProfile(req) {
    var dataServer = req.data.address;
    var url = (username == null || username == "") ?
      dataServer + '/api/user' :
      dataServer + '/api/user?username=' + username;
    requestJSON('GET', url, null, profile, error);
}

// Get the address of the profile
function loadProfile(u) {
    username = u;
    var url = (username == null || username == "") ?
      '/api/user/address' :
      '/api/user/address?username=' + username;
  
    requestJSON('GET', url, null, getProfile, error);
  }
  