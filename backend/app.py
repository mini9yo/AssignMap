from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv
import json


# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)

# Set your OpenAI API key
client=OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization= os.environ.get("ORG_KEY"),
    project= os.environ.get("PROJ_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_type')
def user_type():
    return render_template('user_type.html')

@app.route('/assignment_input')
def assignment_input():
    return render_template('assignment_input.html')

@app.route('/file_upload')
def file_upload():
    return render_template('file_upload.html')

@app.route('/date_input')
def date_input():
    return render_template('date_input.html')

@app.route('/task_display')
def task_display():
    return render_template('task_display.html')

# Route to generate subtasks based on user input
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json  # Get the incoming JSON data
    #print("Received data:", data)  # Debugging output

    # Check for required fields
    if not data or 'user_type' not in data:
        return jsonify({'error': 'Missing required field: user_type'}), 400

    user_type = data.get('user_type')
    
    # Retrieve relevant data
    title = data.get('title')
    num_subtasks = data.get('num_subtasks')
    assignment_description = data.get('assignment_description')

    if user_type == 'teacher':
        return generate_rubric(title, num_subtasks, assignment_description)  # Process for teacher
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
        "Must: after each verbal task text, add a space then an emoji that relates to the functionality of each task to make the list more engaging and visually appealing.\n"
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

        #print("Generated subtasks:", tasks_data)  # Debugging output
        
        # Return the parsed JSON as a response to the frontend
        return jsonify({'tasks': tasks_data['tasks']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors
    
    
def generate_rubric(title, num_subtasks, assignment_description):
    prompt = (
        f"Please generate a rubric with number of {num_subtasks} criteria for the task named '{title}'. "
        "Be aware that the max tokens for this task is 300.\n"
        "It must contain {num_subtasks} number of criteria, each with a criterion, a description, and the points assigned to that criterion. "
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
        "All points should be added up to 100.\n"
        "Only provide the JSON output, without any additional text, no explanations, or other sentences.\n"
        f"The task description is as follows: {assignment_description}\n"
    )

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        ) 
        # Extract and parse the JSON output from the API response
        json_output = response.choices[0].message.content.strip() 
        rubric_data = json.loads(json_output)

        print("Generated rubric:", rubric_data)  # Debugging output
        # Return the parsed JSON as a response to the frontend
        return jsonify({'rubric': rubric_data['rubric']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors

    
if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application
