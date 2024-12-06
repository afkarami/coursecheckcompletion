# -*- coding: utf-8 -*-
"""Course Check Completion Streamlite.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B-iqNAHc0HNVD48YpSyVocW_5pvY9kot
"""

import streamlit as st
import pandas as pd

# Function to load and clean data
def load_data():
    DATABASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMvqtDGEsFiviYP0gOt-4oX0lgNj0y-kXtGxWrSqh0L1hBQ8XwZlUS6wtbUegI6RPmihvYkiVTeDtE/pub?gid=0&single=true&output=csv"
    RESPONSE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQzFjCOyt01_IM2k6QZujhDTMhDtFtKmjBOWdsK2Q2z1AdA1egyJ1yM5nTZlonOUnvgqlLkjwDSwRMx/pub?gid=0&single=true&output=csv"

    # Load both course database and response data
    course_database = pd.read_csv(DATABASE_SHEET_URL)
    response_data = pd.read_csv(RESPONSE_SHEET_URL)

    # Clean up data (strip and lowercase for consistency)
    course_database['Matakuliah'] = course_database['Matakuliah'].str.strip().str.lower()
    response_data['Nama mata kuliah yang diampu sesuai nama dosen yang dipilih sebelumnya'] = response_data['Nama mata kuliah yang diampu sesuai nama dosen yang dipilih sebelumnya'].str.strip().str.lower()

    # Ensure NIM columns are of the same type for comparison
    course_database['NIM'] = course_database['NIM'].astype(str)  # Ensure it's a string for comparison
    response_data['NIM'] = response_data['NIM'].astype(str)  # Ensure it's a string for comparison

    return course_database, response_data

# Streamlit UI
st.title("Student Course Dashboard")
student_id = st.text_input("Enter your Student ID:")

if st.button("Show"):
    if student_id:
        # Load and clean data
        course_database, response_data = load_data()

        # Filter for the student's courses
        student_courses = course_database[course_database['NIM'] == student_id]

        if not student_courses.empty:
            # Check if the courses are filled in response data
            student_courses['IKM Sudah Terisi'] = student_courses['Matakuliah'].apply(
                lambda x: 'Sudah' if x in response_data['Nama mata kuliah yang diampu sesuai nama dosen yang dipilih sebelumnya'].values else 'Belum'
            )

            # Show the result
            st.subheader(f"Courses currently taken by Student ID {student_id}:")
            st.dataframe(student_courses[['Matakuliah', 'IKM Sudah Terisi']])
        else:
            st.warning(f"No courses found for Student ID {student_id}")
    else:
        st.warning("Please enter a valid Student ID.")
