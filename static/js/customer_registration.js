// Handle Post Job Form Submission
document.getElementById('post-job-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const title = document.getElementById('title').value;
    const company = document.getElementById('company').value;
    const location = document.getElementById('location').value;

    // Send data to backend using Fetch API
    fetch('/api/post-job', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, company: company, location: location }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('response-message').textContent = 'Job posted successfully!';
            document.getElementById('post-job-form').reset();
        } else {
            document.getElementById('response-message').textContent = 'Failed to post job. Please try again.';
        }
    })
    .catch((error) => {
        document.getElementById('response-message').textContent = 'Error: ' + error;
    });
});
