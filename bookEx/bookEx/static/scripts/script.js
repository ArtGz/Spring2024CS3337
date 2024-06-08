//Hamburger menu function
function hamburger() {
	var navlinks = document.getElementById("nav-links");
	if (navlinks.style.display === "block") {
		navlinks.style.display = "none";
	}
	else {
		navlinks.style.display = "block";
	}
}