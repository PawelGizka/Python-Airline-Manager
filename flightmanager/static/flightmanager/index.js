function onSearchClick() {
    var date_from = document.getElementById("date_from").value;
    var date_to = document.getElementById("date_to").value;

    var locationAddress = location.href.split('?')[0];
    var isQuery = false;

    if (date_from) {
        isQuery = true;
        locationAddress = locationAddress + "?date_from=" + date_from
    }

    if (date_to) {
        if (isQuery) {
            locationAddress = locationAddress + "&date_to=" + date_to
        } else {
            isQuery = true;
            locationAddress = locationAddress + "?date_to=" + date_to
        }
    }

    location.href=locationAddress
}
