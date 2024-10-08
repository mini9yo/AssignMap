const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const fileInput = document.getElementById('assignment-file');
const fileNameDisplay = document.getElementById('file-name');

if (nextButton) {
    nextButton.addEventListener('click', () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = () => {
                const assignmentDescription = reader.result;
                sessionStorage.setItem('assignmentDescription', assignmentDescription);
                window.location.href = '/date_input';
            };

            reader.readAsText(file);
        } else {
            displayErrorMessage('Please choose a file.');
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = '/assignment_input';
    });
}

function updateFileName() {
    if (fileInput.files.length > 0) {
        fileNameDisplay.innerText = fileInput.files[0].name;
    } else {
        fileNameDisplay.innerText = 'No file chosen';
    }
}

fileInput.addEventListener('change', updateFileName);