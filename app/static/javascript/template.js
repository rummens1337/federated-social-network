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
	document.body.style.backgroundColor = "#364958";
	document.getElementById("jumbotron").style.backgroundColor = "#364958";
	document.getElementById("search").style.backgroundColor = "#364958";
	// document.getElementById("b1").style.backgroundColor = "#3b3b3f" ;
	// document.getElementById("b2").style.backgroundColor = "#3b3b3f" ;
	// document.getElementById("b3").style.backgroundColor = "#3b3b3f" ;

}
function close() {
    document.getElementById("mySidenav").style.width = "0";
  	document.getElementById("main").style.marginRight = "0";
  	document.body.style.backgroundColor = "#3b3b3f" ;
  	document.getElementById("jumbotron").style.backgroundColor = "#364958" ;
  	document.getElementById("search").style.backgroundColor = "#364958" ;
 //  	document.getElementById("b1").style.backgroundColor = "#0b132b" ;
	// document.getElementById("b2").style.backgroundColor = "#0b132b" ;
	// document.getElementById("b3").style.backgroundColor = "#0b132b" ;


}


function myFunction(x) {
  	x.classList.toggle("change");
}