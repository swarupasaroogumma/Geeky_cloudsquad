document.getElementById('attackButton').addEventListener('click', function () {
    const responseMessage = document.getElementById('responseMessage');

    // Simulating sending a request to the target endpoint
    fetch('/target', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                responseMessage.innerHTML = "Request sent to target endpoint!";
            } else {
                responseMessage.innerHTML = "Failed to send request.";
            }
        })
        .catch(error => {
            responseMessage.innerHTML = "Error: Unable to reach the target.";
        });
});
