from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://localhost:8000"}})
  # Enable Cross-Origin Resource Sharing

# Set your OpenAI API key
client=OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization= os.environ.get("ORG_KEY"),
    project= os.environ.get("PROJ_KEY"))

# Route to generate subtasks based on user input
@app.route('/generate', methods=['POST'])

def generate():
    data = request.json  # Get the incoming JSON data
    print("Received data:", data)  # Debugging output

    # Check for required fields
    if not data or 'user_type' not in data:
        return jsonify({'error': 'Missing required field: user_type'}), 400

    user_type = data.get('user_type')
    
    if user_type not in ['teacher', 'student']:
        return jsonify({'error': 'Invalid user_type. Must be "teacher" or "student"'}), 400

    # Required fields for processing
    required_fields = ['title', 'num_subtasks', 'assignment_description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Retrieve relevant data
    title = data.get('title')
    num_subtasks = data.get('num_subtasks')
    assignment_description = data.get('assignment_description')

    if user_type == 'teacher':
        return generate_rubric(title, assignment_description)  # Process for teacher
    elif user_type == 'student':
        return generate_subtasks(title, num_subtasks, assignment_description)  # Process for student

    return jsonify({'error': 'Invalid request'}), 400  # Fallback error handling


def generate_subtasks(title, num_subtasks, assignment_description):
    # Construct the prompt for OpenAI API
    prompt = (
        f"Please generate a list of {num_subtasks} subtasks for the assignment named '{title}' to tackle the assignment efficiently. "
        "Format your response in JSON as follows:\n"
        "{\n"
        "    \"tasks\": [\n"
        "        \"Subtask 1\",\n"
        "        \"Subtask 2\",\n"
        "        \"Subtask 3\",\n"
        "        \"Subtask 4\",\n"
        "        \"Subtask 5\",\n"
        "        \"Subtask 6\",\n"
        "        \"Subtask 7\"\n"
        "    ]\n"
        "}\n"
        "For example, if the user requests 5 subtasks, the output should look like this:\n"
        "{\n"
        "    \"tasks\": [\n"
        "        \"Understand the assignment requirements.\",\n"
        "        \"Research relevant topics.\",\n"
        "        \"Create an outline.\",\n"
        "        \"Write the first draft.\",\n"
        "        \"Review and edit the final submission.\"\n"
        "    ]\n"
        "}\n"
        "Only provide the JSON output, without any additional text, no explanations, or other sentences.\n"
        f"The assignment description is as follows: {assignment_description}\n"
    )

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        # Extract and parse the JSON output from the API response
        json_output = response.choices[0].message.content.strip()  
        tasks_data = json.loads(json_output)

        # Return the parsed JSON as a response to the frontend
        return jsonify(tasks_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors
    
    
def generate_rubric(data):
    data = request.json
    
    if not data or 'title' not in data or 'num_criteria' not in data or 'assignment_description' not in data:
        return jsonify({'error': 'Missing required fields: title, num_criteria, or task_description'}), 400
    
    title = data.get('title')  # Get the task title
    num_criteria = data.get('num_criteria')  # Get the number of criteria
    task_description = data.get('assignment_description')  # Get the task description
    user_defined_criteria = data.get('criteria', [])  # Get user-defined criteria if provided

    # Construct the prompt for OpenAI API
    if user_defined_criteria:
        criteria_list = ', '.join(user_defined_criteria)
        prompt = (
            f"Please generate a rubric with the following criteria for the task named '{title}': {criteria_list}. "
            "Format your response in JSON as follows:\n"
            "{\n"
            "    \"rubric\": [\n"
            "        {\n"
            "            \"criterion\": \"Criterion 1\",\n"
            "            \"description\": \"Description of Criterion 1\",\n"
            "            \"points\": \"Points for Criterion 1\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Criterion 2\",\n"
            "            \"description\": \"Description of Criterion 2\",\n"
            "            \"points\": \"Points for Criterion 2\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "For example, if the user requests 3 criteria, the output should look like this:\n"
            "{\n"
            "    \"rubric\": [\n"
            "        {\n"
            "            \"criterion\": \"Clarity\",\n"
            "            \"description\": \"The task is clearly defined and easy to understand.\",\n"
            "            \"points\": \"10\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Completeness\",\n"
            "            \"description\": \"All aspects of the task are covered.\",\n"
            "            \"points\": \"10\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Accuracy\",\n"
            "            \"description\": \"The task is completed accurately.\",\n"
            "            \"points\": \"10\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "Only provide the JSON output, without any additional text, no explanations, or other sentences.\n"
            f"The task description is as follows: {task_description}\n"
        )
    else:
        prompt = (
            f"Please generate a rubric with {num_criteria} criteria for the task named '{title}'. "
            "Format your response in JSON as follows:\n"
            "{\n"
            "    \"rubric\": [\n"
            "        {\n"
            "            \"criterion\": \"Criterion 1\",\n"
            "            \"description\": \"Description of Criterion 1\",\n"
            "            \"points\": \"Points for Criterion 1\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Criterion 2\",\n"
            "            \"description\": \"Description of Criterion 2\",\n"
            "            \"points\": \"Points for Criterion 2\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "For example, if the user requests 3 criteria, the output should look like this:\n"
            "{\n"
            "    \"rubric\": [\n"
            "        {\n"
            "            \"criterion\": \"Clarity\",\n"
            "            \"description\": \"The task is clearly defined and easy to understand.\",\n"
            "            \"points\": \"10\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Completeness\",\n"
            "            \"description\": \"All aspects of the task are covered.\",\n"
            "            \"points\": \"10\"\n"
            "        },\n"
            "        {\n"
            "            \"criterion\": \"Accuracy\",\n"
            "            \"description\": \"The task is completed accurately.\",\n"
            "            \"points\": \"10\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "Only provide the JSON output, without any additional text, no explanations, or other sentences.\n"
            f"The task description is as follows: {task_description}\n"
        )

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        # Extract and parse the JSON output from the API response
        json_output = response.choices[0].message.content.strip()  
        rubric_data = json.loads(json_output)

        # Return the parsed JSON as a response to the frontend
        return jsonify(rubric_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors

    


if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application
