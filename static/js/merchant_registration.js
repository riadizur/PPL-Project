// Handle Post Job Form Submission
document.getElementById('post-interview-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const title = document.getElementById('title').value;
    const date = document.getElementById('date').value;
    const interviewer = document.getElementById('interviewer').value;

    // Send data to backend using Fetch API
    fetch('/api/post-interview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, date: date, interviewer: interviewer }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('response-message').textContent = 'Data posted successfully!';
            document.getElementById('post-interview-form').reset();
        } else {
            document.getElementById('response-message').textContent = 'Failed to post data. Please try again.';
        }
    })
    .catch((error) => {
        document.getElementById('response-message').textContent = 'Error: ' + error;
    });
});
