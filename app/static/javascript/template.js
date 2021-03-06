function toggleNav(){
  navSize = document.getElementById("mySidenav").style.width;

  if (navSize == "250px") {
    return close();
  }

  return open();
}

// Opens side navigation.
function open() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginRight = "250px";
  document.body.style.backgroundColor = "rgba(54, 73, 88, 1)";
  document.getElementById("nav-btn").style.position = "fixed";
  document.getElementById("jumbotron").style.backgroundColor = "rgba(54, 73, 88, 0.5)";
  document.getElementById("search").style.backgroundColor = "rgba(54, 73, 88, 0.5)";
}

// Closes side navigation.
function close() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginRight = "0";
  document.body.style.backgroundColor = "rgba(54, 73, 88, 1)" ;
  document.getElementById("nav-btn").style.position = "absolute";
  document.getElementById("jumbotron").style.backgroundColor = "rgba(54, 73, 88, 1)" ;
  document.getElementById("search").style.backgroundColor = "rgba(54, 73, 88, 1)" ;
}

function transFunction(x) {
  x.classList.toggle("change");
}

/* Get the username of the logged in user. */
function getUsername() {
  if (checkLogin()) {
    var decoded = jwt_decode(Cookies.get('access_token_cookie'));
    return decoded["identity"];
  }
  return null;
}

/*  Check if the user is logged in and the JWT token is not expired.
  TODO: should be validated too... */
function checkLogin() {
  if (Cookies.get('access_token_cookie') != '' && Cookies.get('access_token_cookie') != null) {
    var decoded = jwt_decode(Cookies.get('access_token_cookie'));
    if (Date.now() >= decoded['exp'] * 1000) {
      // logout
      window.location = "/logout";
      return false;
    } else { return true; }
  }
  return false;
}

function removeNavItems() {
  if (!checkLogin()) {
    document.getElementById("navme").classList.add("w3-hide");
    document.getElementById("navlogout").classList.add("w3-hide");
    document.getElementById("navsettings").classList.add("w3-hide");
    document.getElementById("navfriends").classList.add("w3-hide");
  }
}

$(document).ready(function() {
  removeNavItems();
});