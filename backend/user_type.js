const teacherButton = document.getElementById('teacher-button');
const studentButton = document.getElementById('student-button');
const nextButton = document.getElementById('next-button');
const backButton = document.getElementById('back-button');
const emailInput = document.getElementById('email');
const nameInput = document.getElementById('name');
const passwordInput = document.getElementById('password');

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
        const email = emailInput.value;
        const name = nameInput.value;
        const password = passwordInput.value;

        if (userType && email && name && password) {
            sessionStorage.setItem('userType', userType);
            sessionStorage.setItem('email', email);
            sessionStorage.setItem('name', name);
            sessionStorage.setItem('password', password);
            window.location.href = 'assignment_input.html'; // Redirect to assignment input page
        } else {
            alert('Please select a user type and provide your email, name, and password.'); // Alert if no user type, email, name, or password is provided
        }
    });
}

if (backButton) {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html'; // Redirect to the index page
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
