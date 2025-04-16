// Fetch job listings from Flask backend
function loadJobListings() {
    fetch('/api/jobs')
        .then(response => response.json())
        .then(jobs => {
            const jobTableBody = document.getElementById('job-listings');
            jobTableBody.innerHTML = '';  // Clear any existing content
            jobs.forEach(job => {
                jobTableBody.innerHTML += `
                    <tr>
                        <td>${job.title}</td>
                        <td>${job.company}</td>
                        <td>${job.location}</td>
                        <td><button class="btn btn-success">Apply</button></td>
                    </tr>
                `;
            });
        });
}

// Fetch interview schedules from Flask backend
function loadInterviewSchedule() {
    fetch('/api/interviews')
        .then(response => response.json())
        .then(interviews => {
            const interviewTableBody = document.getElementById('interview-schedule-list');
            interviewTableBody.innerHTML = '';  // Clear any existing content
            interviews.forEach(interview => {
                interviewTableBody.innerHTML += `
                    <tr>
                        <td>${interview.title}</td>
                        <td>${interview.date}</td>
                        <td>${interview.interviewer}</td>
                    </tr>
                `;
            });
        });
}

// Fetch results from Flask backend
function loadResults() {
    fetch('/api/results')
        .then(response => response.json())
        .then(results => {
            const resultsTableBody = document.getElementById('results-list');
            resultsTableBody.innerHTML = '';  // Clear any existing content
            results.forEach(result => {
                resultsTableBody.innerHTML += `
                    <tr>
                        <td>${result.title}</td>
                        <td>${result.status}</td>
                    </tr>
                `;
            });
        });
}

// Load all data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadJobListings();
    loadInterviewSchedule();
    loadResults();
});
