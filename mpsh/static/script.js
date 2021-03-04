function myMenu() {
    let m = document.getElementById("menu");
    if (m.style.display == "flex") {
        m.style.display = "none";
    }
    else {
        m.style.display = "flex";
    }
}

function setMaxPoints() {
    label = document.getElementById("max-points");
    input = document.getElementById("type-points");

    select = document.getElementById("task-select");
    maxpoints = select.options[select.selectedIndex].dataset.maxpoints;

    label.innerHTML = maxpoints;
    input.setAttribute("max", maxpoints);
}