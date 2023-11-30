const menu = document.getElementsByClassName("menu")[0];

const menuPhone = document.getElementById("menu-phone");

menu.addEventListener("click", function () {
    let a = menu.getElementsByTagName("path")[0]
    let b = menu.getElementsByTagName("path")[1]
    let c = menu.getElementsByTagName("path")[2]

    a.classList.toggle("top1")
    b.classList.toggle("middle1")
    c.classList.toggle("bottom1")

    menuPhone.classList.toggle("display-toggle-off")
    menuPhone.classList.toggle("display-toggle-on")
    // a.classList.toggle("line")
    // b.classList.toggle("middle")
    // c.classList.toggle("bottom")
})