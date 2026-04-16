import streamlit as st
import pandas as pd

st.set_page_config(page_title="TeamCapacity Hub", layout="wide")

st.title("TeamCapacity Hub")
st.subheader("Project tracking and utilization dashboard")

df = pd.DataFrame({
    "Project ID": ["P001", "P002"],
    "Project Name": ["Delhaize Reset", "Carrefour Proposal"],
    "Execution TM": ["Anjali", "Mayank"],
    "Project Status": ["In Progress", "Not Started"],
    "Effort Required (hrs)": [20, 15],
    "Actual Effort Logged (hrs)": [12, 4]
})

st.dataframe(df, use_container_width=True)
