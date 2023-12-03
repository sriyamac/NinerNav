// Called by the map iframe to communicate the submitted coordinates, which are forwarded to the
// server.
function sendCoords(lat, long) {
    console.log(lat);
    console.log(long);

    // Get the CSRF token
    let token = document.querySelector("#csrf_token").value;

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        // Make sure the request is fully processed
        if (this.readyState != 4) {
            return;
        }

        // Redirect if everything was marked as okay
        if (this.responseText == "ok") {
            window.location = window.location.origin + "/resultpage";
        }
    }

    xhr.open("POST", "/gamepage", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        latitude: lat,
        longitude: long,
        csrf_token: token
    }));
}