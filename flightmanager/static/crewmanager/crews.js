window.onunload = function(){};
$(document).ready(function() {
    display();
    alert("dizplay")
});


function display() {
    $.get('/airlinemanager/ajax/get_crews/', function(res) {
        displayCrews(res)
    }).fail(function(res) {
        console.log(res);
        alert("Cannot fetch crews")
    });

}

function displayCrews(res) {
    console.log(res)

    $("#content").empty();
    for (let i in res.crews) {
        let crew = res.crews[i];

        if (crew.members.length > 0) {
            var crewMembers = "";

            for (let j in crew.members) {
                let member = crew.members[j];
                crewMembers = crewMembers.concat(`<li><h5>${member.name} ${member.surname}</h5></li> `);
            }

            $("#content").append(`
                <div class="crew-div">
                    <h3>Captain: ${crew.captain_name} ${crew.captain_surname}</h3>
                    <h4>Members: </h4>
                    <ul>
                        ${crewMembers}
                    </ul>
                </div>
                        
            `);

        } else {
            $("#content").append(`
                <div class="crew-div">
                    <h3>Captain: ${crew.captain_name} ${crew.captain_surname}</h3>
                    <h4>There are no crew members: </h4>
                </div>
                        
            `);
        }


    }
}