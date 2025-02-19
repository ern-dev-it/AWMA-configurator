import streamlit as st

columns=['DoorSizeID', 'Mortice', "Latch Plate",
    "Exterior Plate/Handle (Optional)",
    "Interior Plate/Handle",
    "Additional Hardware (Optional)"]

def update_table(row_index, col_index, value):
    if 0 <= row_index < len(st.session_state['table']) and 0 <= col_index < len(columns):
        st.session_state['table'][row_index][col_index] = value

def update_table_by_key(row_index, key, value):
    # Ensure the row index is valid
    if 0 <= row_index < len(st.session_state['table']):
        # Check if the column exists in the list of columns
        if key in columns:
            # Find the index of the column based on the key
            col_index = columns.index(key)
            if value is None or value == "":
                st.session_state['table'][row_index][col_index] = None
            else:
                st.session_state['table'][row_index][col_index] = value