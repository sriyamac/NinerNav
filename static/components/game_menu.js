/* to hide subbuttons until user clicks on main button */
const difficultyButton = document.getElementById('difficultyButton');
const difficultySubButtons = document.getElementById('difficultySubButtons');

    difficultyButton.addEventListener('click', function() {
        if (difficultySubButtons.style.display === 'none') {
            difficultySubButtons.style.display = 'block';
        } else {
            difficultySubButtons.style.display = 'none';
        }
    });

const gameModeSubButtons = document.getElementById('gameModeSubButtons');

// Redirect to leaderboard page
function redirectToLeaderboard() {
    window.location.href = "/leaderboard";
}

//Redirct to login page
function redirectToSignUp() {
    window.location.href = "/signup";
}

//Redirect to gameprep page
function redirectToGamePrep() {
    window.location.href = '/gameprep';
}

//Redirect to gamepage.html
function redirectToGameScreen() {
    window.location.href = '/gamepage';
}

function countdown(minutes) { //change parameter accordingly
    var seconds = 60;
    var mins = minutes
    function tick() {
        var counter = document.getElementById("counter"); //attached to id counter
        var current_minutes = mins-1
        seconds--;
        counter.innerHTML = current_minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        if( seconds > 0 ) {
            setTimeout(tick, 1000);
        } else {
            if(mins > 1){
                countdown(mins-1);           
            }
        }
    }
    tick();
}
