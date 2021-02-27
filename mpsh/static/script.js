function myMenu() {
    let m = document.getElementById("menu");
    if (m.style.display == "flex") {
        m.style.display = "none";
    }
    else {
        m.style.display = "flex";
    }
}