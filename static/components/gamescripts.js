
var gallery = [
    '/static/gallery/testimg1.jpeg',
    '/static/gallery/testimg2.jpeg',
    '/static/gallery/image3.jpg'
];
var currentImageIndex = 0;


// Randomize the order of the gallery
gallery.sort(function() { return 0.5 - Math.random() });

// Set the src of the a-sky element to the first image in the randomized gallery
document.querySelector('#sky').setAttribute('src', gallery[currentImageIndex]);

function rotateCamera(yaw) {
    var sky = document.querySelector('#sky');
    sky.setAttribute('rotation', {y: yaw});
}
function pauseGame() {
    // Add code here to pause game
    // This could involve pausing game logic, animations...
    document.getElementById('pause-menu').style.display = 'block';
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % gallery.length;
    document.querySelector('#sky').setAttribute('src', gallery[currentImageIndex]);
}

function resumeGame() {
    document.getElementById('pause-menu').style.display = 'none';
    // Add code here to resume game
}

// function loadGame() {
//     // Add code here to load game
//     alert('Load button clicked');
// }

// function saveGame() {
//     // Add code here to save game
//     alert('Save button clicked');
// }

function restartGame() {
    // Add code here to restart game
    location.reload();
}

// function openSettings() {
//     // Add code here to open your game's settings
//     alert('Settings button clicked');
// }

// function quitGame() {
//     // Add code here to quit game
//     window.close();
// }

function returnToMainMenu() {
    window.location.href = 'main.html';
}

function changeVolume(volume) {
    // Add code here to change the volume of game
    console.log('Volume changed to ' + volume);
}
