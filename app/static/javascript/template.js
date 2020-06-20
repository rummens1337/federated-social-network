function toggleNav(){
    navSize = document.getElementById("mySidenav").style.width;
    if (navSize == "250px") {
        return close();
    }
    return open();
}
function open() {
    document.getElementById("mySidenav").style.width = "250px";
	document.getElementById("main").style.marginRight = "250px";
	document.body.style.backgroundColor = "rgba(54, 73, 88, 1)";
	document.getElementById("jumbotron").style.backgroundColor = "rgba(54, 73, 88, 0.5)";
	document.getElementById("search").style.backgroundColor = "rgba(54, 73, 88, 0.5)";
	// document.getElementById("b1").style.backgroundColor = "#3b3b3f" ;
	// document.getElementById("b2").style.backgroundColor = "#3b3b3f" ;
	// document.getElementById("b3").style.backgroundColor = "#3b3b3f" ;

}
function close() {
    document.getElementById("mySidenav").style.width = "0";
  	document.getElementById("main").style.marginRight = "0";
  	document.body.style.backgroundColor = "rgba(54, 73, 88, 1)" ;
  	document.getElementById("jumbotron").style.backgroundColor = "rgba(54, 73, 88, 1)" ;
  	document.getElementById("search").style.backgroundColor = "rgba(54, 73, 88, 1)" ;
 //  	document.getElementById("b1").style.backgroundColor = "#0b132b" ;
	// document.getElementById("b2").style.backgroundColor = "#0b132b" ;
	// document.getElementById("b3").style.backgroundColor = "#0b132b" ;

}

function myFunction(x) {
  	x.classList.toggle("change");
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function checkLogin() {
    if (getCookie('access_token_cookie') != '') {
        return true
    }
    else {
        return false
    }
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