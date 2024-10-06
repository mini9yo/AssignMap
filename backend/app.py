from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv
import json


# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__) 
CORS(app, resources={r"/generate": {"origins": "http://localhost:8000"}})
  # Enable Cross-Origin Resource Sharing

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_user, check_password_hash, get_user_by_email, db
 
# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    email = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
db.init_app(app)

with app.app_context():
    db.create_all()


login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'email' not in data or 'name' not in data or 'user_type' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    name = data['name']
    user_type = data['user_type']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(email=email, name=name, user_type=user_type)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 400

    login_user(user)
    return jsonify({'message': 'Logged in successfully'}), 200

# Route to handle user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Protected route example
@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': f'Hello, {current_user.name}! You are a {current_user.user_type}.'}), 200
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    
    if not data or 'email' not in data or 'name' not in data or 'user_type' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    email = data['email']
    name = data['name']
    user_type = data['user_type']
    password = data['password']
    
    if get_user_by_email(email):
        return jsonify({'error': 'Email already registered'}), 400
    
    create_user(email, name, user_type, password)
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/test_db')
def test_db():
    try:
        # Add a test user
        test_user = User(email='test@example.com', name='Test User', user_type='teacher')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()

        # Retrieve users
        users = User.query.all()
        return jsonify({'users': [user.email for user in users],
                        'name': [user.name for user in users]})
    except Exception as e:
        return str(e), 500



# Set your OpenAI API key
client=OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization= os.environ.get("ORG_KEY"),
    project= os.environ.get("PROJ_KEY"))

# Route to generate subtasks based on user input
@app.route('/generate', methods=['POST'])


def generate():
    data = request.json
    
    if not data or 'user_type' not in data:
        return jsonify({'error': 'Missing required field: user_type'}), 400
    
    user_type = data.get('user_type')
    
    if user_type not in ['teacher', 'student']:
        return jsonify({'error': 'Invalid user_type. Must be "teacher" or "student"'}), 400
    
    if 'file_path' not in data:
        return jsonify({'error': 'Missing required field: file_path'}), 400
    
    file_path = data.get('file_path')
    file_content = data.get('user_type')

    
    if user_type == 'teacher':
        return generate_rubric(file_content)
    elif user_type == 'student':
        return generate_subtasks(file_content)


def generate_subtasks(data):
    data = request.json
    
    if not data or 'title' not in data or 'num_subtasks' not in data or 'assignment_description' not in data:
        return jsonify({'error': 'Missing required fields: title, num_subtasks, or assignment_description'}), 400
    
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
