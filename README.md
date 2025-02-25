# AI-Powered Task Creation & Code Validator

🚀 This application utilizes AI to enhance task descriptions, validate code from GitHub repositories, analyze code quality, and generate AI-powered reviews and scores for your code.

## Features

- **Task Input & Enhancement**: Input a task requirement and enhance it by breaking it down into sub-tasks, providing detailed explanations, and suggesting test cases and edge scenarios.
- **GitHub Code Submission**: Validate and fetch code from public GitHub repositories for analysis.
- **Code Quality & Security Analysis**: Perform linting using PyLint and security analysis using Bandit on the fetched code.
- **AI-Powered Code Scoring**: Generate AI reviews and scores based on how well the code implements the task requirements and follows best practices.

## Requirements

- Python 3.7+
- Streamlit
- `google-generativeai`
- GitPython
- PyLint
- Bandit

## Installation
1. Clone this repository and create env
   
2.pip install -r requirements.txt

3.streamlit run app.py


Note:
Ensure that the GitHub repository is public and accessible for the application to fetch the code successfully.
The application currently focuses on Python files for review.
