const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const startDateInput = document.getElementById('start-date');
const dueDateInput = document.getElementById('due-date');
const numSubtasksInput = document.getElementById('num-subtasks');

function validateNumSubtasks() {
    const numSubtasks = numSubtasksInput.value;
    if (!Number.isInteger(Number(numSubtasks)) || Number(numSubtasks) < 1) {
        alert('Please enter a valid integer greater than 0 for the number of subtasks.');
        numSubtasksInput.value = '';
        return false;
    }
    return true;
}

function validateDates() {
    const today = new Date(); // Get today's date
    today.setDate(today.getDate() - 1);
    today.setHours(0, 0, 0, 0);
    const startDate = new Date(startDateInput.value);
    const dueDate = new Date(dueDateInput.value);

    if (startDate && dueDate) {
        if (startDate < today || dueDate < today) {
            alert('Start and due dates cannot be in the past.'); 
            startDateInput.value = '';
            dueDateInput.value = '';
            return false;
        }
        if (startDate > dueDate) {
            alert('Start date cannot be later than the due date.');
            startDateInput.value = '';
            dueDateInput.value = '';
            return false;
        }
    }
    return true;
}

numSubtasksInput.addEventListener('input', validateNumSubtasks);

if (nextButton) {
    nextButton.addEventListener('click', () => {
        const startDate = startDateInput.value;
        const dueDate = dueDateInput.value;
        const numSubtasks = numSubtasksInput.value;

        // Validate inputs
        if (!startDate || !dueDate || !numSubtasks) {
            alert('Please fill in all fields.');
        } else if (validateNumSubtasks() && validateDates()) {
            // Prepare data to send to the backend
            const data = {
                title: 'Your Assignment Title Here', // Replace with your logic to collect title
                num_subtasks: parseInt(numSubtasks, 10), // Ensure this is an integer
                assignment_description: 'Your Assignment Description Here', // Replace with your logic to collect description
                start_date: startDate,
                due_date: dueDate
            };

            // Send data to the backend
            fetch('http://localhost:5000/generate', { // Adjust the URL if needed
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
                return response.json(); // Assuming the backend returns JSON
            })
            .then(responseData => {
                console.log('Success:', responseData);
                // You can redirect to the task display page or update the UI as needed
                window.location.href = 'task_display.html';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was a problem sending the data.');
            });
        }
    });
}


if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'file_upload.html';
    });
}