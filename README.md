# AssignMap
StormHacks 2024

![AssignMap](backend/static/image/AssignMap.png)

## What is AssignMap?
AssignMap, "Assignment" + "GuidMap," is an AI-powered assignment subtask and rubric generator designed to enhance the educational experience by helping students and teachers efficiently manage their assignments. Using OpenAI's API, AssignMap creates customized subtasks and rubrics to fit the unique needs of each assignment. By combining elements of social good and artificial intelligence, AssignMap offers practical educational tools that make learning and teaching more effective and enjoyable.

## Why did we create AssignMap?
In today's fast-paced educational environment, students and teachers both often struggle with managing multiple assignments and understanding their requirements. AssignMap addresses these challenges by:

- **Enhancing Task Management**: Break down assignments into manageable subtasks.
- **Providing Clear Guidelines**: Generate rubrics that clarify assessment criteria.
- **Supporting Diverse Learning Styles**: Help students organize their work in a way that suits their learning preferences.


## How to Use AssignMap

1. Clone the repository:

    ```bash
    git clone git@github.com:mini9yo/AssignMap.git
    ```

2. Navigate to the backend directory:

    ```bash
    cd backend
    ```

3. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Open your browser and go to `http://localhost:8000/` to start organizing your assignments.

- Note: Ensure you have the necessary API keys configured for the OpenAI API.

## Example Files
Users can find example assignment description text files in the folder named `example_files`, located directly under the root directory. These files can be used for a better understanding of how to use the application. All copyrights of the text files belong to SFU professors.

## What's Next?

Our team is passionate about continuing to develop AssignMap beyond the StormHacks 2024 hackathon. We envision a robust user management system where users can:

- **View Generated Plans**: Access and manage their generated subtask plans and rubrics from a personal library.
- **Customize Their Experience**: Edit, add, or delete AI-generated subtasks and criteria, ensuring that the tool meets their specific needs.
- **Upload Multi-Modal Content**: Allow users to upload various file types, enabling a more integrated and flexible approach to assignment management.

## Technologies Used

- Python
- JavaScript
- HTML
- CSS
- OpenAI API
- Figma

## Our Team

- Kaylee Ryu
- Kaiden Palmer
