const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const assignmentTitleInput = document.getElementById('assignment-title');
const courseNameInput = document.getElementById('course-name');

if (nextButton) {
    nextButton.addEventListener('click', () => {
        const assignmentTitle = assignmentTitleInput.value.trim();
        const courseName = courseNameInput.value.trim();

        if (assignmentTitle && courseName) {
            sessionStorage.setItem('assignmentTitle', assignmentTitle);
            sessionStorage.setItem('courseName', courseName);
            window.location.href = 'file_upload.html'; // Navigate to file upload page
        } else {
            alert('Please fill in all fields.'); // Alert if fields are empty
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'user_type.html'; // Navigate back to user type page
    });
}