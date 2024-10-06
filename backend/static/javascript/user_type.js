const teacherButton = document.getElementById('teacher-button');
const studentButton = document.getElementById('student-button');
const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');

let userType = null;

if (teacherButton) {
    teacherButton.addEventListener('click', () => {
        userType = 'teacher';
        setActiveButton(teacherButton);
    });
}

if (studentButton) {
    studentButton.addEventListener('click', () => {
        userType = 'student';
        setActiveButton(studentButton);
    });
}

if (nextButton) {
    nextButton.addEventListener('click', () => {
        if (userType) {
            sessionStorage.setItem('userType', userType);
            window.location.href = '/assignment_input'; 
        } else {
            displayErrorMessage('Please select a user type.');
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = '/'; 
    });
}

function setActiveButton(activeButton) {
    if (teacherButton) {
        teacherButton.classList.remove('active'); 
    }
    
    if (studentButton) {
        studentButton.classList.remove('active'); 
    }
    
    if (activeButton) {
        activeButton.classList.add('active'); 
    }
}
