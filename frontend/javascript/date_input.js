const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const startDateInput = document.getElementById('start-date');
const dueDateInput = document.getElementById('due-date');
const numSubtasksInput = document.getElementById('num-subtasks');

nextButton.addEventListener('click', () => {
    const startDate = startDateInput.value;
    const dueDate = dueDateInput.value;
    const numSubtasks = numSubtasksInput.value;

    if (!startDate || !dueDate || !numSubtasks) {
        alert('Please fill in all fields.');
        return;
    }

    const numSubtasksInt = parseInt(numSubtasks, 10);
    if (!Number.isInteger(numSubtasksInt) || numSubtasksInt < 1) {
        alert('Please enter a valid integer greater than 0 for the number of subtasks.');
        numSubtasksInput.value = '';
        return;
    }

    const today = new Date().setHours(0, 0, 0, 0);
    const startDateObj = new Date(startDate);
    const dueDateObj = new Date(dueDate);

    if (startDateObj < today || dueDateObj < today) {
        alert('Start and due dates cannot be in the past.');
        startDateInput.value = '';
        dueDateInput.value = '';
        return;
    }

    if (startDateObj > dueDateObj) {
        alert('Start date cannot be later than the due date.');
        startDateInput.value = '';
        dueDateInput.value = '';
        return;
    }

    const userType = sessionStorage.getItem('userType');
    const assignmentTitle = sessionStorage.getItem('assignmentTitle');
    const courseName = sessionStorage.getItem('courseName');
    const fileContent = sessionStorage.getItem('fileContent'); // Retrieve file content

    const data = {
        user_type: userType,
        title: assignmentTitle,
        course_name: courseName,
        start_date: startDate,
        due_date: dueDate,
        num_subtasks: numSubtasksInt,
        file_content: fileContent // Include file content in the data object
    };

    fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(responseData => {
        console.log('Success:', responseData);
        window.location.href = 'task_display.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was a problem sending the data.');
    });
});

backButton.addEventListener('click', () => {
    window.location.href = 'file_upload.html'; // Redirect to file upload page
});