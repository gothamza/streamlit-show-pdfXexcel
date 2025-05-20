import streamlit as st
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer
import pypdf

# Initialize session state for page number and total pages
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'total_pages' not in st.session_state:
    st.session_state.total_pages = 0

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    # Read the PDF to get the total number of pages
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        st.session_state.total_pages = len(pdf_reader.pages)
        # Reset to the first page when a new file is uploaded
        st.session_state.current_page = 1
        uploaded_file.seek(0) # Reset file pointer after reading pages
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.session_state.total_pages = 0
        st.session_state.current_page = 1

    if st.session_state.total_pages > 0:
        binary_data = uploaded_file.getvalue()

        # Display navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button('Previous Page'):
                if st.session_state.current_page > 1:
                    st.session_state.current_page -= 1
        with col2:
            # Display current page and total pages, or use a number input
            # For simplicity, let's display for now.
            st.write(f"Page {st.session_state.current_page} of {st.session_state.total_pages}")
            # Or use a number input to jump to a specific page:
            # page_input = st.number_input(label='Go to page:', min_value=1, max_value=st.session_state.total_pages, value=st.session_state.current_page, step=1)
            # st.session_state.current_page = page_input
        with col3:
            if st.button('Next Page'):
                if st.session_state.current_page < st.session_state.total_pages:
                    st.session_state.current_page += 1

        # Display the current page using streamlit-pdf-viewer
        # pdf_viewer renders pages based on 1-based index, so we pass a list with the current page
        pdf_viewer(input=binary_data, width=700, pages_to_render=[st.session_state.current_page])
