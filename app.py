import pandas as pd
import streamlit as st
import tempfile
import os
import json

st.title("Excel Sheet Viewer (with Formulas)")


# Initialize session state for the temporary file path and sheet data
if 'temp_file_path' not in st.session_state:
    st.session_state.temp_file_path = None
if 'sheet_data' not in st.session_state:
    st.session_state.sheet_data = None


uploaded_excel = st.file_uploader("Upload Excel", type=["xlsx", "xls"], key="excel_uploader")

# If a new file is uploaded, process it
if uploaded_excel is not None and st.session_state.temp_file_path is None:
    # Clean up previous temporary file if it exists (shouldn't happen with this logic, but good practice)
    if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
        os.remove(st.session_state.temp_file_path)

    # Create a new temporary file
    suffix = os.path.splitext(uploaded_excel.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_excel.getvalue())
        st.session_state.temp_file_path = tmp_file.name

    # Read sheet names immediately after creating the temp file
    try:
        with pd.ExcelFile(st.session_state.temp_file_path) as xls:
            st.session_state.sheet_names = xls.sheet_names
            st.session_state.selected_sheet = st.session_state.sheet_names[0] if st.session_state.sheet_names else None
    except Exception as e:
        st.error(f"Error reading sheet names: {e}")
        st.session_state.temp_file_path = None # Invalidate path on error

# If a file has been uploaded and processed (temp_file_path is set)
if st.session_state.temp_file_path:
    # Display the sheet selection only if sheet names were successfully read
    if 'sheet_names' in st.session_state and st.session_state.sheet_names:
        selected_sheet = st.selectbox(
            "Select a sheet",
            st.session_state.sheet_names,
            index=st.session_state.sheet_names.index(st.session_state.selected_sheet) if st.session_state.selected_sheet in st.session_state.sheet_names else 0,
            key="sheet_selector"
        )
        st.session_state.selected_sheet = selected_sheet # Update selected sheet in session state

        if selected_sheet:
            st.info(f"Reading sheet '{selected_sheet}' with formulas...")
            # Now, call the tool to read the data with formulas
            # I will make the tool call in the next step once this code is applied.
            st.write("\nOutput of mcp_excel_excel_read_sheet tool with showFormula=True for sheet '" + selected_sheet + "':")
            # Process the tool output and display the dataframe here in the next turn.

# Cleanup temporary file when a new file is uploaded or script ends (Streamlit helps with end of session)
def cleanup_temp_file():
    if 'temp_file_path' in st.session_state and st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
        try:
            os.remove(st.session_state.temp_file_path)
            st.session_state.temp_file_path = None
        except OSError as e:
             st.warning(f"Could not clean up temporary file {st.session_state.temp_file_path}: {e}")

# This doesn't guarantee deletion in all cases (e.g., unexpected crashes), but improves handling
# Streamlit's rerun behavior makes explicit cleanup tricky. Relying on OS for eventual cleanup too.

# The actual tool call and processing of its output will happen in the next turn after the user selects a sheet.
