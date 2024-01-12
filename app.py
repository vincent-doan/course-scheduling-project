import streamlit as st
import pandas as pd
import tempfile
import os
import csv
import time
from solution_by_backtracking import *
from solution_by_value_ordering import *

# -------------------- Initialize session state -------------------- #
if 'courses_temp_path' not in st.session_state:
    st.session_state['courses_temp_path'] = None
if 'classrooms_temp_path' not in st.session_state:
    st.session_state['classrooms_temp_path'] = None
if 'professors_temp_path' not in st.session_state:
    st.session_state['professors_temp_path'] = None
if 'solution_algorithm' not in st.session_state:
    st.session_state['solution_algorithm'] = None
if 'generate_clicked' not in st.session_state:
    st.session_state['generate_clicked'] = False
if 'solution_obtained' not in st.session_state:
    st.session_state['solution_obtained'] = False
if 'time_taken' not in st.session_state:
    st.session_state['time_taken'] = None

def reset_all_states():
    st.session_state['courses_temp_path'] = None
    st.session_state['classrooms_temp_path'] = None
    st.session_state['professors_temp_path'] = None
    st.session_state['solution_algorithm'] = None
    st.session_state['generate_clicked'] = False
    st.session_state['solution_obtained'] = False

# -------------------- File Upload -------------------- #
st.markdown("<h1 style='text-align: center'>Timetable Generator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left'>Input</h3>", unsafe_allow_html=True)
## Courses
uploaded_file = st.file_uploader("Upload a CSV file containing information of all courses", type=["csv"], on_change=lambda: reset_all_states())
if uploaded_file is not None:
    if not uploaded_file.name.endswith('.csv'):
        st.warning("Please upload a CSV file.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.read())
            st.session_state['courses_temp_path'] = temp_file.name
## Classrooms
uploaded_file = st.file_uploader("Upload a CSV file containing information of all classrooms", type=["csv"], on_change=lambda: reset_all_states())
if uploaded_file is not None:
    if not uploaded_file.name.endswith('.csv'):
        st.warning("Please upload a CSV file.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.read())
            st.session_state['classrooms_temp_path'] = temp_file.name
## Professors
uploaded_file = st.file_uploader("Upload a CSV file containing information of all professors", type=["csv"], on_change=lambda: reset_all_states())
if uploaded_file is not None:
    if not uploaded_file.name.endswith('.csv'):
        st.warning("Please upload a CSV file.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(uploaded_file.read())
            st.session_state['professors_temp_path'] = temp_file.name

# -------------------- Algorithm Selection -------------------- #
if st.session_state['courses_temp_path'] and st.session_state['classrooms_temp_path'] and st.session_state['professors_temp_path']:
    if not os.path.exists("output/output.csv"):
        with open("output/output.csv", 'w', newline='') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['Faculty', 'Class ID', 'Course ID', 'Course Name', 'Credits', 'Num. Students',
                                 'Num. Periods','Professor', 'Session', 'Start', 'End', 'Classroom', 'Capacity'])
    
    algorithm = st.selectbox("Select an algorithm", ["Backtracking", "Value Ordering"], on_change=lambda: reset_all_states())
    if algorithm == "Backtracking":
        st.session_state['solution_algorithm'] = SolutionByBacktracking(path_to_all_courses=st.session_state['courses_temp_path'],
                                                                        path_to_all_classrooms=st.session_state['classrooms_temp_path'],
                                                                        path_to_all_professors=st.session_state['professors_temp_path'],
                                                                        output_path="output/output.csv")
    elif algorithm == "Value Ordering":
        st.session_state['solution_algorithm'] = SolutionByValueOrdering(path_to_all_courses=st.session_state['courses_temp_path'],
                                                                        path_to_all_classrooms=st.session_state['classrooms_temp_path'],
                                                                        path_to_all_professors=st.session_state['professors_temp_path'],
                                                                        output_path="output/output.csv")

# -------------------- Get solution -------------------- #
if st.session_state['solution_algorithm'] and st.session_state['solution_obtained'] == False and st.button("Generate"):
    with st.spinner('Please wait...'):
        start = time.time()
        st.session_state['solution_algorithm'].get_solution()
        st.session_state['time_taken'] = time.time() - start
    st.session_state['solution_obtained'] = True

# -------------------- Generate Timetable -------------------- #
if st.session_state['solution_obtained']:
    st.markdown("<h3 style='text-align: left'>Output</h3>", unsafe_allow_html=True)
    st.text(f"Time taken: {st.session_state['time_taken']:.2f} seconds")

    # ---------- Get output.csv & modify ---------- #
    df = pd.read_csv("output/output.csv")
    df['Start'] = df['Start'].apply(lambda x: x+1)
    df['End'] = df['End'].apply(lambda x: x+1)
    df['Periods'] = df['Start'].astype(str) + "-" + df['End'].astype(str)
    df['Classroom'] = df['Classroom'] + ' (' + df['Capacity'].astype(str) + ')'
    df = df.drop(columns=['Start', 'End', 'Capacity'])

    # ---------- Sidebar for filtering and sorting ---------- #
    st.sidebar.header("Options")
    column_to_filter = st.sidebar.selectbox("Select a column to filter", df.columns)
    filter_value = st.sidebar.text_input(f"Enter value to filter in {column_to_filter}", "")
    column_to_sort = st.sidebar.selectbox("Select a column to sort", df.columns)
    sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])
    filtered_df = df[df[column_to_filter].astype(str).str.contains(filter_value, case=False)]
    sorted_df = filtered_df.sort_values(by=column_to_sort, ascending=(sort_order == "Ascending"))

    # ---------- Sidebar for pagination ---------- #
    rows_per_page = st.sidebar.radio("Rows per page", [5, 10, 20], index=1)
    page_number = st.sidebar.number_input("Page number", min_value=1, max_value=len(sorted_df) // rows_per_page + 1, value=1)
    start_index = (page_number - 1) * rows_per_page
    end_index = min(start_index + rows_per_page, len(sorted_df))
    paginated_df = sorted_df.iloc[start_index:end_index]
    paginated_df = paginated_df.set_index(pd.Index(range(start_index + 1, end_index + 1)))

    # ---------- Display the DataFrame ---------- #
    st.table(paginated_df.style.set_table_styles([
        {'selector': 'thead', 'props': [('background-color', '#9ddbfc')]},
        {'selector': 'thead th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('max-width', '150px'), ('word-wrap', 'break-word')]}
    ]))

    st.text(f"Page {page_number} of {len(sorted_df) // rows_per_page + 1}")

    # -------------------- Download Output CSV File -------------------- #
    if st.session_state.get('solution_algorithm') and st.session_state.get('solution_obtained'):
        with open(st.session_state['solution_algorithm'].output_path, 'r') as file:
            csv_data = file.read()
        st.download_button(
            label="Download schedule",
            data=csv_data,
            file_name="schedule.csv",
            mime="text/csv")

    # ---------- Clean up ---------- #
    os.remove(st.session_state['courses_temp_path'])
    os.remove(st.session_state['classrooms_temp_path'])
    os.remove(st.session_state['professors_temp_path'])
