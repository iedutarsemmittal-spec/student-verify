import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Student Verification App", layout="wide")

@st.cache_data
def load_data():
    file_path = '06060400702_Students_Details 2026-27 (2).xlsx'
    if not os.path.exists(file_path):
        file_path = [f for f in os.listdir('.') if f.endswith('.xlsx')][0]
    df = pd.read_excel(file_path, sheet_name='Students List', header=0)
    if 'Status' not in df.columns:
        df['Status'] = 'Pending'
    if 'Correct Class' not in df.columns:
        df['Correct Class'] = ''
    return df

df = load_data()

st.title("🏫 Student Class Verification App")
st.markdown("Teachers can search any student, confirm their class, or select the correct class if they belong elsewhere.")

classes = sorted(df['Class'].dropna().unique().tolist())
selected_class = st.sidebar.selectbox("Filter by Class", ["All Classes"] + classes)

search_query = st.text_input("🔍 Search Student Name or Father's Name:")

filtered_df = df.copy()
if selected_class != "All Classes":
    filtered_df = filtered_df[filtered_df['Class'] == selected_class]

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df['Student Name'].str.lower().str.contains(q, na=False) | 
        filtered_df['Father Name'].str.lower().str.contains(q, na=False)
    ]

st.write(f"Showing **{len(filtered_df)}** students")

edited_df = st.data_editor(
    filtered_df,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Pending", "Confirm", "Wrong Class"],
            required=True
        ),
        "Correct Class": st.column_config.SelectboxColumn(
            "Correct Class",
            options=[""] + classes,
            required=False
        )
    },
    disabled=["Class", "Student Name", "Father Name"],
    hide_index=True,
    num_rows="fixed",
    key="student_editor"
)

if st.button("💾 Save All Changes"):
    for idx in edited_df.index:
        df.loc[idx, 'Status'] = edited_df.loc[idx, 'Status']
        df.loc[idx, 'Correct Class'] = edited_df.loc[idx, 'Correct Class']
    df.to_excel('Updated_Students_Verification.xlsx', index=False)
    st.success("Changes saved successfully to 'Updated_Students_Verification.xlsx'!")

if st.download_button("📥 Download Updated Excel", data=open('Updated_Students_Verification.xlsx', 'rb').read() if os.path.exists('Updated_Students_Verification.xlsx') else b"", file_name="Updated_Students_Verification.xlsx"):
    pass