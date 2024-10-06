// Function to send data to the backend
async function sendData(data) {
    try {
        const response = await fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Specify content type
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log('Success:', responseData);

        window.location.href = 'task_display.html'; // Redirect to the task display page after successful submission
    } catch (error) {
        console.error('Error:', error);
        alert('There was a problem sending the data.');
    }
}
