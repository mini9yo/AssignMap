from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route to generate subtasks based on user input
@app.route('/generate-subtasks', methods=['POST'])
def generate_subtasks():
    data = request.json
    title = data.get('title')  # Get the assignment title
    num_subtasks = data.get('num_subtasks')  # Get the number of subtasks
    assignment_description = data.get('assignment_description')  # Get the assignment description

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
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=150
        )

        # Extract and parse the JSON output from the API response
        json_output = response.choices[0].text.strip()
        tasks_data = json.loads(json_output)

        # Return the parsed JSON as a response to the frontend
        return jsonify(tasks_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application
