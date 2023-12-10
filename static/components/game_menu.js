/* to hide subbuttons until user clicks on main button */
document.addEventListener("DOMContentLoaded", () => {
    // Default to easy levels
    let diff = getCookie("diff");
    if (diff) {
        setDifficulty(diff);
    } else {
        setDifficulty("Beginner");
    }

    const difficultyButton = document.getElementById('difficultyButton');
    const difficultySubButtons = document.getElementById('difficultySubButtons');

    difficultyButton.addEventListener('click', function() {
        if (difficultySubButtons.style.display === 'none') {
            difficultySubButtons.style.display = 'block';
        } else {
            difficultySubButtons.style.display = 'none';
        }
    });

    for (let child of difficultySubButtons.children) {
        child.addEventListener("click", function () {
            setDifficulty(this.innerHTML);
        });
    }
});

// Based on https://stackoverflow.com/a/15724300
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setDifficulty(diff) {
    document.cookie = `diff=${diff}`;

    for (let child of document.querySelector("#difficultySubButtons").children) {
        if (child.innerHTML != diff) {
            child.classList.remove("selected");
        } else {
            child.classList.add("selected");
        }
    }
}