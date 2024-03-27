// userID = sessionStorage.getItem('userID');
userID = 6

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
console.log('getsessionid');
};

// after clicking submit button
function confirmExtend() {
    new_endtime = document.getElementById('endtime').value;
    console.log(new_endtime);
    // getSessionID(userID);
    sessionID=5;
    console.log(sessionID);
    var isConfirmed = confirm("Confirm extension of session till " + new_endtime + "?");
    if (isConfirmed) {
        askForNotificationPreference(new_endtime,sessionID);
    }
}

function askForNotificationPreference(new_endtime,sessionID) {
    console.log("askfornotif");
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
    console.log("updateselectedcp");
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
                alert('Update successful!');
                console.log(e);
                console.log('update successful!')
                
            }, 
            error: function(xhr, status, error) { 
                alert('fail');
                console.log("Error: " + xhr.responseText);
            }
        });

}
