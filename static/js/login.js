console.log("running...")


document.getElementById('loginform').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    try{
    const email = document.getElementById('emaillogin').value;
    console.log(email);
    const password = document.getElementById('passwordlogin').value;

    sendSession(email,password);
    
    } 
    catch (error) {
        console.error('Error:', error.message);
        // Handle the error
    }
});

async function sendSession(email,password) {
    const data = {
        email: email,
        password: password
    };
    console.log(data);

        $.ajax({ 
            url: 'http://localhost:5010/checkuser',
            type: 'POST', 
            contentType: 'application/json', 
            data: JSON.stringify(data), 
            // xhrFields: {
            //     withCredentials: true
            // },
            success: function(e) { 
                console.log(e)
                alert('Login successful!');
            }, 
            error: function(xhr, status, error) { 
                console.log("Error: " + xhr.responseText);
            }
        });

}