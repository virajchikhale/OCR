import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "No": [101, 102, 103],
    "Stream": ["Engineering", "Science", "Arts"],
    "Details": ["Details about Alice", "Details about Bob", "Details about Charlie"]
}
df = pd.DataFrame(data)

# Display the table with a button in the last column
st.write("Candidates Table")

# Create table structure
for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])  # Adjust column widths
    col1.write(row['Name'])
    col2.write(row['No'])
    col3.write(row['Stream'])
    
    # Add a button in the last column for each row
    if col4.button("View Details", key=f"view_{index}"):
        with st.expander(f"Details of {row['Name']}"):
            st.write(row['Details'])
