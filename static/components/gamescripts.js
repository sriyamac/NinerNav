let rotation = 0;

function rotateCamera(yaw) {
    let sky = document.querySelector('#sky');
    rotation += yaw;
    sky.setAttribute('rotation', {y: rotation});
}