userID = sessionStorage.getItem('userID');

function getSessionID(userID){
$.ajax({ 
    url: 'http://localhost:5006/session/'+userID,
    type: 'GET', 
    dataType: 'json',
    success: function(e) { 
        console.log(e)
        var sessionID = e.data.sessionID;
        // Now you can use sessionID as needed
        console.log(sessionID);
        // alert('Current session retrieved!');
    }, 
    error: function(xhr, status, error) { 
        console.log("Error: " + xhr.responseText);
    }
})
};

// after clicking submit button
function confirmExtend() {
    new_endtime = document.getElementById('endtime').value;
    sessionID = getSessionID(userID);
    var isConfirmed = confirm("Confirm extension of session till " + new_endtime + "?");
    if (isConfirmed) {
        askForNotificationPreference(new_endtime,sessionID);
    }
}

function askForNotificationPreference(new_endtime,sessionID) {
    var isConfirmed = confirm("Do you want to receive notifications about your parking session?");
    if (isConfirmed) {
        // session wants to receive notifications
        updateSelectedCP(new_endtime,sessionID); 
    } else {
        // session does not want to receive notifications
        updateSelectedCP(new_endtime, false, sessionID); 
    }
}


// This updates details of the carpark and parking session to session database
async function updateSelectedCP(new_endtime, notifAllowed, sessionID) {
    const data = {
        endtime: new_endtime, 
        notifAllowed: notifAllowed
    };
    console.log(data);

        $.ajax({ 
            url: 'http://localhost:5006/session/'+sessionID,
            type: 'PUT', 
            contentType: 'application/json', 
            data: JSON.stringify(data), 
            success: function(e) { 
                console.log(e)
                alert('Update successful!');
            }, 
            error: function(xhr, status, error) { 
                console.log("Error: " + xhr.responseText);
            }
        });

}
