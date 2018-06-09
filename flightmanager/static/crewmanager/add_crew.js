var memberCount = 0;

$().ready(function() {
    addMember();
    $('#error').hide();
});


function addMember() {
    $('#crew-members-div').append(`
                <div class="row" id="member-${memberCount}">
                    <div class="col-sm-6">
                        <input name="member_name" id="member-name-${memberCount}" placeholder="Name" type="text">
                    </div>
        
                    <div class="col-sm-6">
                        <input name="member_surname" id="member-surname-${memberCount}" placeholder="Surname" type="text">
                    </div>
                </div>
                        
            `);

    memberCount++;
}

function addCrew() {
    let serializedUserData = localStorage.getItem('user');
    if (serializedUserData == null) {
        location.href='login.html';
        return;
    }


    let captainName = $('#captain_name').val();
    let captainSurname = $('#captain_surname').val();

    if (captainName.length === 0 || captainSurname.length === 0) {
        $('#error').html("Captain name and surname cannot be blank");
        $('#error').show();
        return;
    }

    let members = [];

    for (let i = 0; i < memberCount; i++) {
        let memberName = $(`#member-name-${i}`).val();
        let memberSurname = $(`#member-surname-${i}`).val();

        if (memberName.length !== 0 && memberSurname.length !== 0) {
            members.push(JSON.stringify({'name': memberName, 'surname': memberSurname}));
        }

    }

    let userData = JSON.parse(serializedUserData);
    let data = {
        'username': userData.username,
        'password': userData.password,
        'captainName': captainName,
        'captainSurname': captainSurname,
        'members': members
    };

    $.post('/airlinemanager/ajax/add_crew/', data, function () {
        console.log('chat message sent');
        window.history.back()

    }).fail(function (res) {
        console.log('adding crew failed');
        $('#error').html(res.responseText);
        $('#error').show();
    });

}