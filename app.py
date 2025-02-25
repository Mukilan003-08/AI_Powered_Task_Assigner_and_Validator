import streamlit as st
import google.generativeai as genai
import os
import requests
import git
import subprocess

# Set up Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = "YOur Gemini API Key"
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="AI Task & Code Validator", layout="wide")
st.title("🚀 AI-Powered Task Creation & Code Validation")

# ---------------------- TASK INPUT & ENHANCEMENT ----------------------
st.header("📝 Task Input & Enhancement")
task_input = st.text_area("Enter your task requirement:", height=150)

if st.button("🔍 Enhance Task"):
    if task_input:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                f"Enhance the following task requirement by breaking it down into sub-tasks, explaining each in detail, and suggesting test cases and edge scenarios:\n\n{task_input}"
            )
            enhanced_task = response.text

            st.success("✅ Task Enhancement Successful!")
            st.write("### 🔹 Enhanced Task:")
            st.write(enhanced_task)

        except Exception as e:
            st.error(f"🚨 Gemini API Error: {e}")
    else:
        st.warning("⚠ Please enter a task requirement.")

# ---------------------- GITHUB CODE SUBMISSION ----------------------
st.header("📂 GitHub Code Submission & Analysis")
repo_url = st.text_input("🔗 Enter GitHub Repo URL:")
repo_dir = ""

if repo_url:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_dir = os.path.join(".", repo_name)

if st.button("📥 Validate & Fetch Code"):
    if repo_url:
        try:
            response = requests.get(repo_url)
            if response.status_code == 200:
                st.success("✅ Repository validated successfully!")

                if os.path.exists(repo_dir):
                    st.warning("⚠ Repository already cloned. Using existing copy.")
                else:
                    git.Repo.clone_from(repo_url + ".git", repo_dir)
                    st.success("✅ Repository cloned successfully!")

                # List only relevant code files, ignoring .git and non-code files
                st.write("### 📜 Relevant Code Files in the Repository:")

                allowed_extensions = (".py", ".js", ".html", ".css", ".java", ".cpp", ".ts","xlsx")  # Add more if needed
                ignored_dirs = {".git", "__pycache__"}  # Directories to ignore

                for root, dirs, files in os.walk(repo_dir, topdown=True):
                    dirs[:] = [d for d in dirs if d not in ignored_dirs]  # Ignore .git and __pycache__
                    for file in files:
                        if file.endswith(allowed_extensions):  # Only include relevant code files
                            st.write(f"📄 {os.path.relpath(os.path.join(root, file), repo_dir)}")


            else:
                st.error("🚨 Check for permissions (Public repository) or Invalid GitHub repository URL.")
        except Exception as e:
            st.error(f"⚠ Error fetching repository: {e}")
    else:
        st.warning("⚠ Please enter a valid GitHub repo URL.")

# ---------------------- CODE QUALITY & SECURITY ANALYSIS ----------------------
st.header("🔎 Code Quality & Security Analysis")

if st.button("📊 Analyze Code"):
    if repo_dir and os.path.exists(repo_dir):
        st.write("### 🚀 Running Code Quality Checks...")

        # Linting & Formatting (PyLint)
        pylint_result = subprocess.run(["pylint", repo_dir], capture_output=True, text=True)
        st.subheader("🧹 Linting & Formatting (PyLint)")
        st.code(pylint_result.stdout, language="python")

        # Security Analysis (Bandit)
        bandit_result = subprocess.run(["bandit", "-r", repo_dir], capture_output=True, text=True)
        st.subheader("🔐 Security Analysis (Bandit)")
        st.code(bandit_result.stdout, language="python")

    else:
        st.warning("⚠ Please validate and fetch the repository first.")

# ---------------------- AI CODE SCORING & REVIEW ----------------------
st.header("🏆 AI-Powered Code Scoring")

if st.button("🤖 Generate AI Review & Score"):
    try:
        model = genai.GenerativeModel("gemini-pro")
        code_files = []
        
        if repo_dir and os.path.exists(repo_dir):
            for root, _, files in os.walk(repo_dir):
                for file in files:
                    if file.endswith(".py"):  # Only process Python files
                        with open(os.path.join(root, file), "r") as f:
                            code_files.append(f.read())

        if not code_files:
            st.warning("⚠ No Python files found for review.")
        else:
            code_content = "\n\n".join(code_files)
            
            if not task_input:
                st.warning("⚠ Please enter a task requirement before reviewing the code.")
            else:
                # Pass the task details along with code for validation
                response = model.generate_content(
                    f"Given the following task description:\n\n{task_input}\n\n"
                    f"Review and score this code based on how well it implements the task, "
                    f"as well as best practices, efficiency, and security:\n\n{code_content}"
                )
                ai_feedback = response.text

                st.write("### 🏅 AI Review & Score:")
                st.write(ai_feedback)

    except Exception as e:
        st.error(f"🚨 AI Processing Error: {e}")
