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
        # Reset to the first page when a new file is uploaded, only if it's a new file
        # This check prevents resetting page number when navigating
        if 'last_uploaded_file_id' not in st.session_state or st.session_state.last_uploaded_file_id != uploaded_file.file_id:
             st.session_state.current_page = 1
             st.session_state.last_uploaded_file_id = uploaded_file.file_id

        uploaded_file.seek(0) # Reset file pointer after reading pages
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.session_state.total_pages = 0
        st.session_state.current_page = 1

    if st.session_state.total_pages > 0:

        # Display navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button('Previous Page'):
                if st.session_state.current_page > 1:
                    st.session_state.current_page -= 1
                    st.rerun() # Use st.rerun() instead of st.experimental_rerun()
        with col2:
            # Display current page and total pages
            st.write(f"Page {st.session_state.current_page} of {st.session_state.total_pages}")

        with col3:
            if st.button('Next Page'):
                if st.session_state.current_page < st.session_state.total_pages:
                    st.session_state.current_page += 1
                    st.rerun() # Use st.rerun() instead of st.experimental_rerun()

        binary_data = uploaded_file.getvalue()

        # Display the current page using streamlit-pdf-viewer
        # pdf_viewer renders pages based on 1-based index, so we pass a list with the current page
        pdf_viewer(input=binary_data, width=700, pages_to_render=[st.session_state.current_page])
