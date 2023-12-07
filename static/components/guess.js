
var map;

var marker;

//postion var needs to be connected with the proper coords from the DB
//right now they are hard coded
let position = {lat: 35.308168, lng: -80.733699}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: position,
        zoom: 17
    });

    marker = new google.maps.Marker({
        position: position,
        map: map
    });
    
    map.panTo(position);
}