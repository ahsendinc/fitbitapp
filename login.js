document.getElementById('loginContainer').children[0].children[0].children[0].onclick = function() {
        document.getElementById('loginContainer').children[0].children[0].children[0].classList.add("active")
    document.getElementById('loginContainer').children[0].children[0].children[1].classList.remove("active")
    document.getElementById('loginContainer').children[0].children[2].style.display = "none";
    document.getElementById('loginContainer').children[0].children[1].style.display = "block";
}

document.getElementById('loginContainer').children[0].children[0].children[1].onclick = function() {
    document.getElementById('loginContainer').children[0].children[0].children[0].classList.remove("active")
    document.getElementById('loginContainer').children[0].children[0].children[1].classList.add("active")
    document.getElementById('loginContainer').children[0].children[1].style.display = "none";
    document.getElementById('loginContainer').children[0].children[2].style.display = "block";
}