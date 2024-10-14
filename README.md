# Resume Builder and Analyzer Application

This project implements a **Resume Builder and Analyzer** using **Streamlit** in Python. The application allows users to build a resume using a drag-and-drop interface and analyze existing resumes to extract information and provide suggestions for improvement. Below are the details of the application, environment setup, and execution steps.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Application Overview](#application-overview)
- [Features](#features)
- [Code Structure](#code-structure)
- [Execution](#execution)
- [Screenshots](#screenshots)

---

## Environment Setup

To set up the environment and run this project, follow these steps:

1. **Create a Python Virtual Environment**:

   ```bash
   python -m venv resume_env
   ```

2. **Activate the Virtual Environment**:

   - On macOS/Linux:

     ```bash
     source resume_env/bin/activate
     ```

   - On Windows:

     ```bash
     resume_env\Scripts\activate
     ```

3. **Install Required Libraries**:

   Install all required libraries using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, you can install them individually:*

   ```bash
   pip install streamlit pandas base64 nltk pdfminer.six streamlit-tags streamlit-sortables docx2txt
   ```

4. **Download NLTK Data Files**:

   In the Python environment, run the following commands to download necessary NLTK data files:

   ```python
   import nltk
   nltk.download('stopwords')
   ```

---

## Application Overview

This application provides an interactive platform for users to either build a new resume from scratch or analyze an existing resume for improvements.

### Build Resume

![NLP1](https://github.com/user-attachments/assets/6fd4c440-1e19-4681-aa28-cbf52da4561a)

- **Customizable Layout**: Choose between different layouts for the drag-and-drop interface.

- **Reorder Sections**: Use drag-and-drop to reorder resume sections according to preference.

- **Edit Content**: Input and edit content for each section directly within the app.

- **Preview and Download**: Preview the assembled resume and download it as a text file.

### Analyze Resume

![NLP2](https://github.com/user-attachments/assets/a1c4aadf-6c9d-48a1-9ed2-06c7906bf769)

- **File Upload**: Upload resumes in PDF or DOCX formats.

- **Display Resume**: View the uploaded resume within the app (PDF files).

- **Extracted Information**: Automatically extract key details such as name, email, phone number, skills, and experience.

- **Improvement Suggestions**: Receive tailored suggestions to enhance the resume.

- **Scoring System**: Get a resume score out of 100 based on completeness and content quality.

---

## Features

### Build Resume

- **Drag-and-Drop Interface**: Implemented using `streamlit-sortables`, allows users to reorder sections.

- **Customizable Sections**: Users can add new sections or edit existing ones.

- **Layout Preference**: Choose between different layouts for the drag-and-drop interface.

- **Resume Preview**: Real-time preview of the resume as sections are edited.

- **Download Resume**: Generate and download the resume as a text file.

### Analyze Resume

- **Resume Upload**: Upload resumes in PDF or DOCX formats.

- **Resume Display**: View uploaded PDF resumes directly in the app.

- **Information Extraction**: Automatically extract name, email, phone number, skills, and total experience from the resume.

- **Suggestions for Improvement**: Receive recommendations on missing sections or areas to enhance.

- **Resume Scoring**: Obtain a resume score out of 100 based on completeness and content.

---

## Code Structure

Below is an overview of the code structure and key components of the application:

### Libraries and Imports

The application utilizes several libraries:

- **Streamlit**: For building the web application interface.
- **Pandas**: For data manipulation.
- **NLTK**: For natural language processing tasks.
- **pdfminer.six**: For extracting text from PDF files.
- **docx2txt**: For extracting text from DOCX files.
- **streamlit-sortables**: For implementing the drag-and-drop interface.
- **Regex (re)**: For pattern matching and information extraction.

### Functions

#### `read_pdf(file)`

Reads a PDF file and extracts text using `pdfminer.six`.

```python
def read_pdf(file):
    text = extract_text(file)
    return text
```

#### `show_pdf(file_path)`

Displays a PDF file within the Streamlit app using an HTML iframe.

```python
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
```

#### `extract_information(resume_text)`

Extracts basic information such as name, email, phone, skills, and total experience from the resume text using regular expressions.

```python
def extract_information(resume_text):
    # Patterns to match
    name_pattern = re.compile(r"Name[:\-]?\s*(.*)", re.IGNORECASE)
    email_pattern = re.compile(r"Email[:\-]?\s*([\w\.-]+@[\w\.-]+)", re.IGNORECASE)
    phone_pattern = re.compile(r"(?:Phone|Contact)[:\-]?\s*(\+?\d[\d\s\-]+\d)", re.IGNORECASE)
    skills_keywords = ['python', 'java', 'sql', 'machine learning', 'data analysis', 'communication', 'teamwork']

    # Extract name
    name_match = name_pattern.search(resume_text)
    name = name_match.group(1).strip() if name_match else ''

    # Extract email
    email_match = email_pattern.search(resume_text)
    email = email_match.group(1).strip() if email_match else ''

    # Extract phone number
    phone_match = phone_pattern.search(resume_text)
    phone = phone_match.group(1).strip() if phone_match else ''

    # Extract skills
    skills = []
    for skill in skills_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text, re.IGNORECASE):
            skills.append(skill.title())

    # Calculate total experience (simple estimation)
    experience_years = 0
    experience_matches = re.findall(r'(\d+)\s+years?', resume_text, re.IGNORECASE)
    if experience_matches:
        experience_years = sum([int(num) for num in experience_matches])

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'total_experience': experience_years
    }
```

### Main Application Flow

The `main()` function controls the flow of the application:

1. **Page Configuration**: Sets the page title and layout.

2. **Sidebar Options**: Provides a selection between "Build Resume" and "Analyze Resume".

3. **Build Resume**:

   - **Layout Preference**: Users choose the position of the drag-and-drop interface.

   - **Drag-and-Drop Interface**: Implemented using `streamlit-sortables`, allowing users to reorder resume sections.

   - **Resume Sections**: Default sections are provided, and users can add new sections.

   - **Resume Preview and Editing**: Users can edit the content of each section.

   - **Generate Resume**: Users can generate and download the resume as a text file.

4. **Analyze Resume**:

   - **Resume Upload**: Users upload a resume file.

   - **Resume Display**: If the file is a PDF, it is displayed in the app.

   - **Text Extraction**: Extract text from the uploaded resume using `pdfminer.six` or `docx2txt`.

   - **Information Extraction**: Extracts key details using `extract_information()`.

   - **Suggestions**: Provides suggestions for missing sections.

   - **Resume Scoring**: Calculates a score based on the number of suggestions.

---

## Execution

To run this application, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd resume-builder-app
   ```

3. **Set Up the Environment**:

   Create and activate the virtual environment as outlined in the setup steps.

4. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

   *Note: Replace `app.py` with the actual filename if different.*

5. **Open in Browser**:

   Streamlit will provide a local URL (usually `http://localhost:8501`), which you can open in your web browser to interact with the application.

---

## Screenshots

### Build Resume Interface

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/4c63db1e-05c4-4651-b73e-20dd1d4801b4">

### Analyze Resume Interface

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/684c361c-f08a-4f99-996b-b7aee3d285d3">

---
