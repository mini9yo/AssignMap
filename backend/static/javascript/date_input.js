const startDateInput = document.getElementById('start-date');
const dueDateInput = document.getElementById('due-date');
const numSubtasksInput = document.getElementById('num-subtasks');
const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');

document.addEventListener("DOMContentLoaded", () => {
    const userType = sessionStorage.getItem('userType');
    const numSubtasksLabel = document.querySelector('label[for="num-subtasks"]');

    // Change label text based on user type
    if (userType === 'teacher') {
        numSubtasksLabel.textContent = 'Number of Criteria:';
    } else {
        numSubtasksLabel.textContent = 'Number of Subtasks:';
    }

    nextButton.addEventListener('click', () => {
        const startDate = startDateInput.value;
        const dueDate = dueDateInput.value;
        const numSubtasks = numSubtasksInput.value;

        // Validation checks
        if (!startDate || !dueDate || !numSubtasks) {
            displayErrorMessage('Please fill out all fields.');
            return;
        }

        const numSubtasksInt = parseInt(numSubtasks, 10);
        if (!Number.isInteger(numSubtasksInt) || numSubtasksInt < 1) {
            displayErrorMessage('Please enter a valid integer greater than 0 for the number of subtasks.');
            numSubtasksInput.value = '';
            return;
        } else if (userType === 'student' && numSubtasksInt > 10) {
            displayErrorMessage('Please enter a valid integer less than or equal to 10 for the number of subtasks.');
            numSubtasksInput.value = '';
            return;
        } else if (userType === 'teacher' && numSubtasksInt > 7) { // Adjusted because of the max token in OpenAI
            displayErrorMessage('Please enter a valid integer less than or equal to 7 for the number of criteria.');
            numSubtasksInput.value = '';
            return;
        }

        const today = new Date().setHours(0, 0, 0, 0);
        const startDateObj = new Date(startDate);
        const dueDateObj = new Date(dueDate);

        startDateObj.setDate(startDateObj.getDate() + 1); // Adjust for timezone offset

        // Validation for start and due dates
        if (startDateObj < today || dueDateObj < today) {
            displayErrorMessage('Start and due dates must be today or later.');
            startDateInput.value = '';
            dueDateInput.value = '';
            return;
        }

        if (startDateObj > dueDateObj) {
            displayErrorMessage('Due date must be after the start date.');
            startDateInput.value = '';
            dueDateInput.value = '';
            return;
        }

        sessionStorage.setItem('startDate', startDate);
        sessionStorage.setItem('dueDate', dueDate);

        const assignmentTitle = sessionStorage.getItem('assignmentTitle');
        const assignmentDescription = sessionStorage.getItem('assignmentDescription');

        // data to send to the backend
        const data = {
            user_type: userType,
            title: assignmentTitle,
            num_subtasks: numSubtasksInt,
            assignment_description: assignmentDescription
        };

        sendData(data);
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/file_upload'; 
    });
});

// Function to send data to the backend
async function sendData(data) {
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log('Success:', responseData);

        // Store tasks or rubric in sessionStorage based on user type
        if (data.user_type === 'teacher') {
            sessionStorage.setItem('rubric', JSON.stringify(responseData.rubric || []));
        } else {
            sessionStorage.setItem('generatedTasks', JSON.stringify(responseData.tasks || []));
        }

        window.location.href = '/task_display'; 
    } catch (error) {
        console.error('Error:', error);
        displayErrorMessage('An error occurred. Please try again.');
    }
}