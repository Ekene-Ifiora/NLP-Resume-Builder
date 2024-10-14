import streamlit as st
import pandas as pd
import base64
import time
import datetime
import random
from pyresparser import ResumeParser
import io
from streamlit_tags import st_tags
from PIL import Image
import plotly.express as px
import nltk
from nltk.corpus import stopwords
import os
from pdfminer.high_level import extract_text
from streamlit_sortables import sort_items  # Correct import from streamlit-sortables
import docx2txt
import re


# Download NLTK data files
nltk.download('stopwords')

# Function to read PDF and extract text
def read_pdf(file):
    """
    Function to read PDF file and extract text
    """
    text = extract_text(file)
    return text

# Function to display PDF in the Streamlit app
def show_pdf(file_path):
    """
    Function to display PDF in Streamlit app
    """
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to generate a download link for dataframes
def get_table_download_link(df, filename, text):
    """
    Generates a link allowing the data in a given pandas dataframe to be downloaded
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to extract information from resume text
def extract_information(resume_text):
    """
    Extract basic information from the resume text using regex patterns
    """
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

# Main function of the application
def main():
    # Set page configuration
    st.set_page_config(page_title="Resume Builder", layout="wide")

    # Title of the application
    st.title("Resume Builder Application")

    # Sidebar for user options
    st.sidebar.title("Options")
    option = st.sidebar.selectbox("Choose an option", ("Build Resume", "Analyze Resume"))

    # Resume Builder section
    if option == "Build Resume":
        st.header("Build Your Resume")

        # Choose layout preference
        layout_pref = st.radio("Choose Layout", ("Drag-and-Drop on Left", "Drag-and-Drop on Right"))

        # Split the screen based on layout preference
        if layout_pref == "Drag-and-Drop on Left":
            drag_col, resume_col = st.columns([1, 2])
        else:
            resume_col, drag_col = st.columns([2, 1])

        # Initialize the resume content as a list of sections
        if 'resume_sections' not in st.session_state:
            st.session_state.resume_sections = [
                {"title": "Contact Information", "content": ""},
                {"title": "Objective", "content": ""},
                {"title": "Education", "content": ""},
                {"title": "Experience", "content": ""},
                {"title": "Skills", "content": ""},
                {"title": "Projects", "content": ""},
                {"title": "Certifications", "content": ""},
                {"title": "Hobbies", "content": ""},
            ]

        # Drag-and-drop interface for sections
        with drag_col:
            st.subheader("Drag and Drop Sections")
            # Get the list of section titles
            section_titles = [section["title"] for section in st.session_state.resume_sections]
            # Use sort_items to allow drag-and-drop reordering
            reordered_titles = sort_items(
                items=section_titles,
                direction="vertical",
                key="sortable-sections",
            )
            # Reorder the sections based on the drag-and-drop result
            new_order = []
            for title in reordered_titles:
                for section in st.session_state.resume_sections:
                    if section["title"] == title:
                        new_order.append(section)
                        break
            st.session_state.resume_sections = new_order

            # Option to add new section
            new_section_title = st.text_input("Add New Section")
            if st.button("Add Section"):
                if new_section_title:
                    # Add new section to resume sections
                    st.session_state.resume_sections.append({"title": new_section_title, "content": ""})
                    st.success(f"Added new section: {new_section_title}")
                else:
                    st.error("Please enter a section title.")

        # Resume preview and editing
        with resume_col:
            st.subheader("Resume Preview")
            for section in st.session_state.resume_sections:
                # Use expanders for each section
                with st.expander(section["title"], expanded=True):
                    # Text area to edit section content
                    content = st.text_area(f"Edit {section['title']}", value=section["content"], key=section["title"])
                    section["content"] = content

            # Option to generate resume
            if st.button("Generate Resume"):
                # Generate the resume content by concatenating sections
                resume_text = ""
                for section in st.session_state.resume_sections:
                    resume_text += f"\n\n{section['title']}\n{section['content']}"
                # Display the resume
                st.subheader("Generated Resume")
                st.text(resume_text)
                # Option to download the resume as a text file
                b64 = base64.b64encode(resume_text.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="resume.txt">Download Resume</a>'
                st.markdown(href, unsafe_allow_html=True)

   # Resume Analyzer section
    if option == "Analyze Resume":
        st.header("Analyze Your Resume")

        # File uploader for resume
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

        if uploaded_file is not None:
            # Save uploaded file
            file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
            st.write(file_details)

            # Ensure the upload directory exists
            if not os.path.exists("Uploaded_Resumes"):
                os.makedirs("Uploaded_Resumes")

            # Save file to disk
            save_path = os.path.join("Uploaded_Resumes", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Show resume if it's a PDF
            if uploaded_file.type == "application/pdf":
                show_pdf(save_path)
                resume_text = read_pdf(save_path)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # For docx files
                resume_text = read_docx(save_path)
                st.write("Preview not available for DOCX files.")
            else:
                st.write("Unsupported file type.")
                return

            # Extract information from resume text
            resume_data = extract_information(resume_text)

            if resume_data:
                st.subheader("Resume Analysis")

                # Display basic information
                st.write(f"**Name:** {resume_data.get('name', '')}")
                st.write(f"**Email:** {resume_data.get('email', '')}")
                st.write(f"**Phone:** {resume_data.get('phone', '')}")
                st.write(f"**Total Experience:** {resume_data.get('total_experience', 0)} years")
                st.write(f"**Skills:** {', '.join(resume_data.get('skills', []))}")

                # Suggest improvements
                st.subheader("Suggestions to Improve Your Resume")
                # Example suggestions based on content
                suggestions = []

                if 'Objective' not in resume_text:
                    suggestions.append("Add an 'Objective' section to outline your career goals.")
                if 'Projects' not in resume_text:
                    suggestions.append("Include a 'Projects' section to showcase your work.")
                if 'Achievements' not in resume_text:
                    suggestions.append("Add an 'Achievements' section to highlight your accomplishments.")
                if 'Certifications' not in resume_text:
                    suggestions.append("Include any relevant 'Certifications' you have obtained.")
                if 'Hobbies' not in resume_text:
                    suggestions.append("Adding a 'Hobbies' section can show your personality.")

                if suggestions:
                    for suggestion in suggestions:
                        st.write(f"- {suggestion}")
                else:
                    st.write("Your resume looks great!")

                # Resume scoring based on the number of suggestions
                resume_score = 100 - len(suggestions) * 10
                if resume_score < 0:
                    resume_score = 0
                st.write(f"**Resume Score:** {resume_score}/100")
            else:
                st.error("Unable to analyze the resume.")
        else:
            st.info("Please upload your resume in PDF or DOCX format.")

# Run the application
if __name__ == '__main__':
    main()
