// URL of the Flask server (adjust the port if necessary)
const registerUrl = 'http://127.0.0.1:5000/register';
const loginUrl = 'http://127.0.0.1:5000/login';
const generateUrl = 'http://127.0.0.1:5000/generate';

// Sample data to send in the POST request for user registration
const registerData = {
  email: "test@example.com",
  name: "Test User",
  user_type: "teacher",
  password: "password123"
};

// Function to send a POST request for user registration and handle the response
async function testRegisterEndpoint() {
  try {
    const response = await fetch(registerUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(registerData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Registration Response:', data);
    } else {
      // Log additional error information from the server response
      const errorText = await response.text();
      console.error('Error:', response.status, response.statusText, errorText);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Sample data to send in the POST request for user login
const loginData = {
  email: "test@example.com",
  password: "password123"
};

// Function to send a POST request for user login and handle the response
async function testLoginEndpoint() {
  try {
    const response = await fetch(loginUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Login Response:', data);
    } else {
      // Log additional error information from the server response
      const errorText = await response.text();
      console.error('Error:', response.status, response.statusText, errorText);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Sample data to send in the POST request for the generate endpoint
const requestData = {
  user_type: "teacher",
  file_path: "C:/Users/kaide/OneDrive/Desktop/example.txt", // Replace this with a valid file path
  title: "Math Assignment", // Example title
  num_subtasks: 5, // Number of subtasks to generate
  assignment_description: "This assignment covers basic algebra and geometry.", // Description of the assignment
  num_criteria: 3,
};

// Function to send a POST request to the generate endpoint and handle the response
async function testGenerateEndpoint() {
  try {
    const response = await fetch(generateUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Generate Response:', data);
    } else {
      // Log additional error information from the server response
      const errorText = await response.text();
      console.error('Error:', response.status, response.statusText, errorText);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

// Run the test functions sequentially
testRegisterEndpoint().then(() => {
  testLoginEndpoint().then(() => {
    testGenerateEndpoint();
  });
});



