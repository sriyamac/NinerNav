var map;
//marker var
var marker;
//user placed marker var
var uMark;
//var to hold distance between umark and rmark
var scoreDist;
//line draw to connect markers
var line;

//var rMark. long and lat of the target.
var rMark = {lat: 35.306320, lng: -80.733389};

function initMap() {
    let UNCC = {lat: 35.308168, lng: -80.733699}
    map = new google.maps.Map(document.getElementById('map'), {
        center: UNCC,
        zoom: 15
    });

    // event listener adds marker when/where user clicks
    map.addListener('click', function(e) {
        placeMarkerAndPanTo(e.latLng, map);
    });
}

function placeMarkerAndPanTo(latLng, map) {
    // If marker already exists -> remove it
    if (marker) {
        marker.setMap(null);
    }

    // Add new marker
    marker = new google.maps.Marker({
        position: latLng,
        map: map
    });

    uMark = latLng;
    map.panTo(latLng);
}

function submitMarker() {
    if (marker) {
        /* let rmark = new google.maps.Marker({
            position: rMark,
            map: map
        });

        //checks for previous line and deletes it
        if(line){
            line.setMap(null);
        }
        //adds line
        line = new google.maps.Polyline({
            path: [rMark, uMark],
            odesic: true,
            strokeColor: "#FF0000",
            map: map
        })

        // Calculate the distance between uMark and rMark in meters
        scoreDist = google.maps.geometry.spherical.computeDistanceBetween(uMark, rMark); */
    } else {
        alert("Please place a marker on the map before submitting.");
        return;
    }

    //calculate the score and send to the parent
    //let score = Math.floor(200 * (1 + ((-1)/(1 + Math.exp(-scoreDist/10)))));
    //parent.relayScore(score);
    parent.sendCoords(uMark.lat(), uMark.lng());
}