from engine import *
import streamlit as st


def initialize_session_state():

    if "logs" not in st.session_state:
        st.session_state.logs=[]

    if 'duplicates' not in st.session_state:
        st.session_state.duplicates=[]


def show_sidebar():

    st.sidebar.title("Settings")
    folder_path=st.sidebar.text_input("Enter the folder path which you want to organize")

    organize_btn=st.sidebar.button("Organise files")
    duplicates_btn=st.sidebar.button("Find duplicates")
    clear_logs_btn=st.sidebar.button("Clear logs")

    return (folder_path,organize_btn,duplicates_btn,clear_logs_btn)

def handle_organize(folder_path):
    if not os.path.exists(folder_path):
        st.error("Invalid folder path")
    
    logs=organise_files(folder_path)
    st.session_state,logs.extend(logs)
    
    st.success("Sucessfully organized")

def handle_find_duplicates(folder_path):
    if not os.path.exists(folder_path):
        st.error("Invalid folder path")

    duplicates=find_duplicates(folder_path)
    st.session_state.duplicates.extend(duplicates)


def display_duplicates(folder_path):

    if not st.session_state.duplicates:
        return
    st.warning(f"Found {len(st.session_state.duplicates)}")
    st.subheader("Duplicates below")

    for file in st.session_state.duplicates:
        st.write(file)
    
    if st.button("Move duplicates"):

        logs=move_duplicates(folder_path,st.session_state.duplicates)

        st.session_state.logs.extend(logs)
        st.success("Sucessfully moved the duplicates")

        st.session_state.duplicates=[]


def display_logs():
    st.subheader("Logs")
    for msg in st.session_state.logs :
        st.write(msg)
    st.session_state.logs=[]

initialize_session_state()

folder_path,organise_btn,duplicates_btn,clear_logs=show_sidebar()

if duplicates_btn:
    handle_find_duplicates(folder_path)

if organise_btn:
    handle_organize(folder_path)

if clear_logs:
    display_logs()