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
    const assignmentDescription = sessionStorage.getItem('assignmentDescription'); // Retrieve file content

    console.log('User Type:', userType);
    console.log('Assignment Title:', assignmentTitle);
    console.log('Course Name:', courseName);
    console.log('Assignment Description:', assignmentDescription);

    const data = {
        user_type: userType,
        title: assignmentTitle,
        course_name: courseName,
        num_subtasks: numSubtasksInt,
        assignment_description: assignmentDescription // Include file content in the data object
    };

    sendData(data);
});

backButton.addEventListener('click', () => {
    window.location.href = 'file_upload.html'; // Redirect to file upload page
});