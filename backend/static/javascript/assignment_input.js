const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const assignmentTitleInput = document.getElementById('assignment-title');
const courseNameInput = document.getElementById('course-name');

if (nextButton) {
    nextButton.addEventListener('click', () => {
        const assignmentTitle = assignmentTitleInput.value.trim();
        const courseName = courseNameInput.value.trim();
        
        console.log('Assignment Title:', assignmentTitle);
        console.log('Course Name:', courseName);

        if (assignmentTitle && courseName) {
            sessionStorage.setItem('assignmentTitle', assignmentTitle);
            sessionStorage.setItem('courseName', courseName);
            window.location.href = '/file_upload';
        } else {
            displayErrorMessage('Please fill out all fields.'); 
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = '/user_type';
    });
}