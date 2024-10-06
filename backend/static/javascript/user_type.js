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
            window.location.href = '/assignment_input'; // Redirect to assignment input page
        } else {
            alert('Please select a user type.'); // Alert if no user type is selected
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = '/'; // Redirect to the index page
    });
}

function setActiveButton(activeButton) {
    if (teacherButton) {
        teacherButton.classList.remove('active'); // Remove active class from teacher button
    }
    
    if (studentButton) {
        studentButton.classList.remove('active'); // Remove active class from student button
    }
    
    if (activeButton) {
        activeButton.classList.add('active'); // Add active class to the clicked button
    }
}
