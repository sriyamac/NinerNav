function initMap() {
    let position = {
        lat: parseFloat(document.querySelector("#lat").value),
        lng: parseFloat(document.querySelector("#lng").value)
    };

    let map = new google.maps.Map(document.getElementById('map'), {
        center: position,
        zoom: 17
    });

    let marker = new google.maps.Marker({
        position: position,
        map: map
    });
    
    map.panTo(position);
}