window.onunload = function(){};
$(document).ready(function() {
    display();
});

function onShowClick() {
    let date = document.getElementById("date").value;
    $.get(`/airlinemanager/ajax/get_assignments/?date=${date}`, function(res) {
        displayAssignments(res)
    }).fail(function(res) {
        console.log(res);
        alert("Cannot fetch assignments")
    });
}

function display() {
    $.get('/airlinemanager/ajax/get_assignments/', function(res) {
        displayAssignments(res)
    }).fail(function(res) {
        console.log(res);
        alert("Cannot fetch assignments")
    });

}

function displayAssignments(res) {
    console.log(res)

    $("#content").empty();
    for (let i in res.flights) {
        let flight = res.flights[i];
        console.log(flight)
        let crew = flight.crew;

        var crewContent = `<h3>There is no crew assigned to this flight</h3>`;
        if (crew) {
            if (crew.members.length > 0) {
            var crewMembers = "";

            for (let j in crew.members) {
                let member = crew.members[j];
                crewMembers = crewMembers.concat(`<li><h5>${member.name} ${member.surname}</h5></li> `);
            }

            crewContent = `
                 <div class="crew-div">
                     <h3>Captain: ${crew.captain_name} ${crew.captain_surname}</h3>
                     <h4>Members: </h4>
                     <ul>
                         ${crewMembers}
                     </ul>
                 </div>
    
             `;

            } else {
                crewContent = `
                     <div class="crew-div">
                         <h3>Captain: ${crew.captain_name} ${crew.captain_surname}</h3>
                         <h4>There are no crew members: </h4>
                     </div>
        
                 `;
            }
        }

        $("#content").append(`
            <div class="flight-box" >

                <div class="row">
                  <div class="col-sm-6">
                    <h3>Flight: ${flight.id}</h3>
                  </div>
                </div>

                <div class="row">
                    <div class="col-sm-6">
                        <p>From: ${flight.from}</p>
                    </div>
                    <div class="col-sm-6">
                        <p>To: ${flight.to}</p>
                    </div>
                </div>
                

                ${crewContent}
                
                <div class="row">
                  <div class="col-sm-12">
                    <button id="manage-crew-button-${flight.id}" type="button" onclick="location.href='manage_assignment.html?flight=${flight.id}' "
                            class="btn btn-outline-info">Manage Crew</button>
                  </div>
                </div>
            </div>
        `);




    }
}