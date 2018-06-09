var noFlightId = false;
var flightId;

$().ready(function() {
    $('#error').hide();
    var flight = location.href.split('?')[1];
    if (flight) {
        flightId = flight.split('=')[1];
        if (flightId) {
            $('#main_text').html(`Menage crew for flight: ${flightId}`);
            loadCrews();
        } else {
            noFlightId = true;
            $('#error').show();
            $('#error').html("There is no flight id in query parameter");
        }
    } else {
        noFlightId = true;
        $('#error').show();
        $('#error').html("There is no flight id in query parameter");
    }


});

function loadCrews() {
    $.get('/airlinemanager/ajax/get_crews/', function(res) {
        displayCrews(res)
    }).fail(function(res) {
        console.log(res);
        alert("Cannot fetch crews")
    });
}

function displayCrews(res) {
    console.log(res)

    $("#select").empty();
    for (let i in res.crews) {
        let crew = res.crews[i];

        $("#select").append(`<option value="${crew.id}">Captian: ${crew.captain_name} ${crew.captain_surname}</option>`)
    }
}

function assign() {
    let serializedUserData = localStorage.getItem('user');
    if (serializedUserData == null) {
        location.href='login.html';
        return;
    }

    let crewId = $('#select option:selected').val();


    let userData = JSON.parse(serializedUserData);
    let data = {
        'username': userData.username,
        'password': userData.password,
        'crewId': crewId,
        'flightId': flightId,
    };

    $.post('/airlinemanager/ajax/assign/', data, function () {
        window.history.back()
    }).fail(function (res) {
        $('#error').html(res.responseText);
        $('#error').show();
    });

}