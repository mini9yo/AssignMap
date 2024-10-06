const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');

if (nextButton) {
    nextButton.addEventListener('click', () => {
        const assignmentTitle = document.getElementById('assignment-title').value;
        const courseName = document.getElementById('course-name').value;

        if (assignmentTitle && courseName) {
            sessionStorage.setItem('assignmentTitle', assignmentTitle);
            sessionStorage.setItem('courseName', courseName);
            window.location.href = 'file_upload.html';
        } else {
            alert('Please fill in all fields.');
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
}