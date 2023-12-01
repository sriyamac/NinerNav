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

const gameButton = document.getElementById('gameButton');
const gameModeSubButtons = document.getElementById('gameModeSubButtons');

gameButton.addEventListener('click', function() {
    if (gameModeSubButtons.style.display === 'none') {
        gameModeSubButtons.style.display = 'block';
    } else {
        gameModeSubButtons.style.display = 'none';
    }
});




// Redirect to leaderboard page
function redirectToLeaderboard() {
    window.location.href = "leaderboard.html";
}

//Redirct to login page
function redirectToSignUp() {
    window.location.href = "sign-up.html";
}

//Redirct to signed-in page
function redirectToSignedIn() {
    window.location.href = "signed-in.html";
}

//Redirect to gameprep page
function redirectToGamePrep() {
    window.location.href = 'gameprep.html';
}

//Redirect to gamepage.html
function redirectToGameScreen() {
    window.location.href = 'gamepage.html';
}

//display user information
// function displayUserInfo() {
//     //locally stored user info for now, need DB in future
//     const userInfo = localStorage.getItem("userInfo");

//     //display functionality 
//     if (userInfo) {
//         const userInfoLines = userInfo.split(', ').join('<br>'); //formating, creating separate lines for each user credential 
//         document.getElementById("displayUserInfo").innerHTML = `<h4>User Info:</h4><p>${userInfoLines}</p>`;
//     } else {
//         document.getElementById("displayUserInfo").innerText = "No user info available.";
//     }
// }

//when page loads, automatically displays user info
// displayUserInfo();

// //redirect to game screen 
// function redirectToGameScreen() {
//     //if the user is logged in, then go button is functional
//     const userInfo = localStorage.getItem("userInfo");
//     if (userInfo) {
//         window.location.href = "gamescreen.html";
//     } else {
//         alert("Please login/signup first.");
//     }
// }