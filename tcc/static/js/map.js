'use strict'

let marker;
let content;
let infowindow;

function initMap() {
    let inputLat = $('#id_latitude').val();
    let inputLng = $('#id_longitude').val();

    let initialZoom;
    content = '<h6 class="vt-align-self__c">'

    if($('#id_name').val().length != 0) {
        initialZoom = 16;
        content = content + $('#id_name').val() + '</h6>';
    } else {
        initialZoom = 8;
        content = content + 'Canoinhas</h6>';
    }

    let mapCenter = new google.maps.LatLng(inputLat,inputLng);
    let mapOptions = {center: mapCenter, zoom: initialZoom};
    let map = new google.maps.Map($('#map')[0], mapOptions);

    map.addListener('click', function(event) {
        addInfoWindow(content);
        placeMarkerAndPanTo(event.latLng, map);
    });
    
    addInfoWindow(content);
    placeMarkerAndPanTo(mapCenter, map);
}

function placeMarkerAndPanTo(latLng, map) {
    if(marker) {
        marker.setMap(null);
    }
    
    marker = new google.maps.Marker({
        position: latLng,
        map: map
    });
    
    marker.addListener('click', function() {
        infowindow.open(map, marker);
        mapZoom(map, latLng, map.getZoom()+2)
    });
    infowindow.open(map, marker);

    map.panTo(latLng);
    
    $('#id_latitude').val(latLng.lat());
    $('#id_longitude').val(latLng.lng());
}

function addInfoWindow(content, latLng) {
    infowindow = new google.maps.InfoWindow({
        content: content
    });
}

function mapZoom(map, latLng, zoom) {
    map.setZoom(zoom);
    map.setCenter(latLng);
}

$('#id_name').change(function() {
    content = '<h6 class="vt-align-self__c">';
    if($(this).val().length != 0) {
        content = content + $(this).val() + '</h6>';
    } else {
        content = content + 'TCC' + '</h6>';
    }
    
    infowindow.setContent(content);
});