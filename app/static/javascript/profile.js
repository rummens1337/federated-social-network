var username = null;

function error(req) { 
    // TODO: use our custom error 
    alert("Error during loading.");
}

function profile(req) {
    alert(req.data.username);
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
  