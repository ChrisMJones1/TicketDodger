$(document).ready(function () {
    var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
    var DateTime = luxon.DateTime;
    var user_time = DateTime.local().setZone('America/Los_Angeles');
    var user_hour = user_time.hour;

    var address_input;



    $("#search_form").submit(search);

    function search(event) {
        address_input = $("#search_input").val();

        // import
        // import { OpenStreetMapProvider } from 'leaflet-geosearch';

        // setup
        const provider = new OpenStreetMapProvider();

        // search
        provider.search({query: address_input}).then(function (result) {
            // address_input = result;
            // result = JSON.parse(result);
            result = result[0];
            result.x = parseFloat(result.x);
            result.y = parseFloat(result.y);
             return render_search(result);
        });
        event.preventDefault();
    }
    function render_search(result) {
        if (result.y >= 33.7030139 && result.y <= 34.7478410 && result.x <= -117.6972698 && result.x >= -118.9409686) {
            $("#lat").val(result.y);
            $("#long").val(result.x);
            $("#hidden_form").submit();
        } else {

            $("#error_message").html("Error finding address / address out of range");
            return false;
        }
    }
});