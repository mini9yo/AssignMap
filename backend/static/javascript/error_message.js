function displayErrorMessage(message) {
    const errorMessageDiv = document.createElement('div');
    errorMessageDiv.className = 'error-message';
    errorMessageDiv.textContent = message; 

    const container = document.querySelector('.mainofmain');
    if (container) {
        container.appendChild(errorMessageDiv);

        setTimeout(() => {
            errorMessageDiv.remove();
        }, 3000);
    } else {
        console.error('Container with class "mainofmain" not found.');
    }
}