document.addEventListener("DOMContentLoaded", () => {
    const generatedTasks = JSON.parse(sessionStorage.getItem('generatedTasks'));
    const rubric = JSON.parse(sessionStorage.getItem('rubric'));

    const assignmentTitle = sessionStorage.getItem('assignmentTitle');
    const courseName = sessionStorage.getItem('courseName');
    const dueDate = sessionStorage.getItem('dueDate');

    document.getElementById('assignment-title').textContent = `${courseName} - ${assignmentTitle}`;
    document.getElementById('due-date').textContent = `Due Date: ${dueDate}`;

    const tasksContainer = document.getElementById('tasks');

    tasksContainer.innerHTML = ''; 
    const userType = sessionStorage.getItem('userType');

    // Display tasks if user type is student
    if (userType === 'student') {
        if (generatedTasks && Array.isArray(generatedTasks) && generatedTasks.length > 0) {
            document.getElementById('gen-type').innerHTML = '<strong>Subtask Planner:</strong>';
            generatedTasks.forEach((task, index) => {
                const taskBox = document.createElement('div');
                taskBox.className = 'task-box'; 
                taskBox.textContent = `${index + 1}: ${task}`; 
                tasksContainer.appendChild(taskBox); 
            });
        } else {
            document.getElementById('gen-type').innerHTML = '<strong>Subtask Planner:</strong>';
            const noTasksBox = document.createElement('div');
            noTasksBox.className = 'task-box';
            noTasksBox.textContent = 'No tasks generated.';
            tasksContainer.appendChild(noTasksBox);
        }
    }
    
    // Display rubric if user type is teacher
    if (userType === 'teacher') {
        if (rubric && Array.isArray(rubric) && rubric.length > 0) {
            document.getElementById('gen-type').innerHTML = '<strong>Rubric:</strong>';
            rubric.forEach((criterion, index) => {
                const rubricBox = document.createElement('div');
                rubricBox.className = 'task-box';
                rubricBox.innerHTML = `<strong>${criterion.criterion}:</strong><br>`;
                rubricBox.innerHTML += `<span style="font-size: smaller;">${criterion.description}</span><br>`;
                rubricBox.innerHTML += `<span style="font-size: medium; color: #5bc0de;">(Points: ${criterion.points} / 100)</span><br>`;
                tasksContainer.appendChild(rubricBox);
            });
        } else {
            document.getElementById('gen-type').innerHTML = '<strong>Rubric:</strong>';
            const noRubricBox = document.createElement('div');
            noRubricBox.className = 'task-box'; 
            noRubricBox.textContent = 'No rubric generated.';
            tasksContainer.appendChild(noRubricBox);
        }
    }
});