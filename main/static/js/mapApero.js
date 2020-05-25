//  Map Apero points delivery

mapboxgl.accessToken = 'pk.eyJ1Ijoib2RpbGVsZWNsZXJjc2l0ZSIsImEiOiJjazZjMDJtNGEwZ3F2M2tvdnNncnkxNXRxIn0.c7i8XUNby5CQwhdrsG3r0A';
var map = new mapboxgl.Map({
    container: 'map-apero',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-1.249550, 44.651470], //longitude, latitude
    zoom: 12,
});


var geojson_apero = {
    type: 'FeatureCollection',
    features: [{
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-1.2427271, 44.6482281]
        },
        properties: {
            title: 'Apero',
            description: 'Corps mort'
        }
    }]
};

map.on('click', 'Feature', function (e) {
    var coordinates = e.features[0].geometry.coordinates.slice();
    var description = e.features[0].properties.description;

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }

    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);
});

geojson_apero.features.forEach(function (marker) {

    // create a HTML element for each feature
    var el = document.createElement('div');
    el.className = 'marker-apero';

    // make a marker for each feature and add to the map
    new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
            .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
        .addTo(map);
});