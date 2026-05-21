# #with update:
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# import uuid

# st.set_page_config(page_title="Task Tracker", page_icon="🚀", layout="wide")

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# EXPECTED_HEADERS = [
#     "ID",
#     "Date",
#     "Task Description",
#     "Files List",
#     "Category",
#     "Deployed Status",
#     "Client",
#     "Branch Name",
#     "Created At"
# ]

# try:
#     creds = Credentials.from_service_account_info(
#         st.secrets["gcp_service_account"],
#         scopes=SCOPES
#     )
#     client = gspread.authorize(creds)
#     SHEET_ID = "1kfoJPOwkIP8lUQcBIZKsjVooVS9MoqRSCXeF4EE5wwk"
#     spreadsheet = client.open_by_key(SHEET_ID)
#     sheet = spreadsheet.sheet1
# except Exception as e:
#     st.error("❌ Google Sheets connection failed")
#     st.exception(e)
#     st.stop()

# try:
#     existing_data = sheet.get_all_values()
#     if len(existing_data) == 0:
#         sheet.append_row(EXPECTED_HEADERS)
#     elif existing_data[0] != EXPECTED_HEADERS:
#         sheet.resize(rows=1)
#         sheet.update("A1:I1", [EXPECTED_HEADERS])
# except Exception as e:
#     st.error(e)

# def load_df():
#     records = sheet.get_all_records()
#     if not records:
#         return pd.DataFrame(columns=EXPECTED_HEADERS)
#     df = pd.DataFrame(records)
#     if "Date" in df.columns:
#         df["Date_sort"] = pd.to_datetime(df["Date"], errors="coerce")
#         df = df.sort_values("Date_sort", ascending=True, na_position="last")
#         df = df.drop(columns=["Date_sort"])
#     return df

# def append_record(row_data):
#     sheet.append_row(row_data)

# def find_row_by_id(record_id):
#     id_col = sheet.col_values(1)
#     for idx, value in enumerate(id_col[1:], start=2):
#         if value == record_id:
#             return idx
#     return None

# def update_record(record_id, row_data):
#     row_num = find_row_by_id(record_id)
#     if not row_num:
#         return False
#     sheet.update(f"A{row_num}:I{row_num}", [row_data])
#     return True

# def delete_record(record_id):
#     row_num = find_row_by_id(record_id)
#     if not row_num:
#         return False
#     sheet.delete_rows(row_num)
#     return True

# st.markdown("""
# <style>
# .main-title {
#     font-size: 40px;
#     font-weight: bold;
#     margin-bottom: 10px;
# }
# .sub-title {
#     color: gray;
#     margin-bottom: 30px;
# }
# .stButton>button {
#     width: 100%;
#     background-color: #4CAF50;
#     color: white;
#     border-radius: 10px;
#     height: 45px;
#     font-size: 16px;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main-title">🚀 Task Tracker</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-title">Track deployments, fixes and customizations</div>', unsafe_allow_html=True)

# df = load_df()

# if not df.empty:
#     st.subheader("📋 Saved Tasks")

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         filter_client = st.text_input("Search Client")
#     with col2:
#         filter_category = st.selectbox("Filter Category", ["All", "Hot Fix", "Bug Fix", "Customization"])
#     with col3:
#         filter_status = st.selectbox("Filter Deployment", ["All", "On Client", "Server-148", "Server-177", "Not Deployed"])

#     filtered_df = df.copy()

#     if filter_client:
#         filtered_df = filtered_df[
#             filtered_df["Client"].astype(str).str.contains(filter_client, case=False, na=False)
#         ]
#     if filter_category != "All":
#         filtered_df = filtered_df[filtered_df["Category"] == filter_category]
#     if filter_status != "All":
#         filtered_df = filtered_df[filtered_df["Deployed Status"] == filter_status]

#     st.dataframe(filtered_df, use_container_width=True, height=500)

#     st.divider()
#     st.subheader("✏️ Edit or Delete Record")

#     if not filtered_df.empty:
#         options = filtered_df["ID"].astype(str) + " | " + filtered_df["Date"].astype(str) + " | " + filtered_df["Client"].astype(str)
#         selected_label = st.selectbox("Select Record", options.tolist())
#         selected_id = selected_label.split(" | ")[0]

#         selected_row = filtered_df[filtered_df["ID"].astype(str) == selected_id].iloc[0]

#         with st.form("edit_form"):
#             c1, c2 = st.columns(2)

#             with c1:
#                 edit_date = st.date_input("Date", value=pd.to_datetime(selected_row["Date"]).date() if pd.notna(selected_row["Date"]) else datetime.today().date())
#                 edit_client = st.text_input("Client Name", value=str(selected_row["Client"]))
#                 edit_category = st.selectbox("Category", ["Hot Fix", "Bug Fix", "Customization"], index=["Hot Fix", "Bug Fix", "Customization"].index(str(selected_row["Category"])) if str(selected_row["Category"]) in ["Hot Fix", "Bug Fix", "Customization"] else 0)

#             with c2:
#                 edit_status = st.selectbox("Deployment Status", ["On Client", "Server-148", "Server-177", "Not Deployed"], index=["On Client", "Server-148", "Server-177", "Not Deployed"].index(str(selected_row["Deployed Status"])) if str(selected_row["Deployed Status"]) in ["On Client", "Server-148", "Server-177", "Not Deployed"] else 0)
#                 edit_branch = st.text_input("Branch Name", value=str(selected_row["Branch Name"]))

#             edit_task = st.text_area("Task Description", value=str(selected_row["Task Description"]), height=120)
#             edit_files = st.text_area("Files List", value=str(selected_row["Files List"]), height=120)

#             save_edit = st.form_submit_button("Update Record")
#             delete_btn = st.form_submit_button("Delete Record")

#         if save_edit:
#             try:
#                 updated_row = [
#                     selected_id,
#                     str(edit_date),
#                     edit_task,
#                     edit_files,
#                     edit_client,
#                     edit_category,
#                     edit_status,
#                     edit_branch,
#                     str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 ]
#                 if update_record(selected_id, updated_row):
#                     st.success("✅ Record updated successfully!")
#                     st.rerun()
#                 else:
#                     st.error("Record not found")
#             except Exception as e:
#                 st.error("❌ Failed to update record")
#                 st.exception(e)

#         if delete_btn:
#             try:
#                 if delete_record(selected_id):
#                     st.success("🗑️ Record deleted successfully!")
#                     st.rerun()
#                 else:
#                     st.error("Record not found")
#             except Exception as e:
#                 st.error("❌ Failed to delete record")
#                 st.exception(e)

# st.divider()
# st.subheader("➕ Add New Task")

# with st.form("deployment_form", clear_on_submit=True):
#     col1, col2 = st.columns(2)

#     with col1:
#         task_date = st.date_input("Date", value=datetime.today().date())
#         client_name = st.text_input("Client Name", placeholder="Enter client name")
#         category = st.selectbox("Category", ["Hot Fix", "Bug Fix", "Customization"])

#     with col2:
#         deployed_status = st.selectbox("Deployment Status", ["On Client", "Server-148", "Server-177", "Not Deployed"])
#         branch_name = st.text_input("Branch Name", placeholder="feature/report-cleanup")

#     task_description = st.text_area("Task Description", placeholder="Explain the task...", height=120)
#     files_list = st.text_area(
#         "Files List",
#         placeholder="""Controllers/ReportController.cs
# Services/ReportService.cs
# Views/Report/Index.cshtml""",
#         height=120
#     )

#     submitted = st.form_submit_button("Save Task")

# if submitted:
#     if task_description.strip() == "":
#         st.error("Task Description is required")
#     else:
#         try:
#             created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             record_id = str(uuid.uuid4())
#             row = [
#                 record_id,
#                 str(task_date),
#                 task_description,
#                 files_list,
#                 category,
#                 deployed_status,
#                 client_name,
#                 branch_name,
#                 created_at
#             ]
#             append_record(row)
#             sheet.append_row(row)

#             st.success("✅ Task saved successfully!")
#             st.rerun()
#         except Exception as e:
#             st.error("❌ Failed to save task")
#             st.exception(e)

##un stable version:
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import gspread
# from google.oauth2.service_account import Credentials
# import uuid

# # =====================================================
# # PAGE CONFIG
# # =====================================================

# st.set_page_config(
#     page_title="Task Tracker",
#     page_icon="🚀",
#     layout="wide"
# )

# # =====================================================
# # GOOGLE SHEETS CONFIG
# # =====================================================

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# EXPECTED_HEADERS = [
#     "ID",
#     "Date",
#     "Task Description",
#     "Files List",
#     "Category",
#     "Deployed Status",
#     "Client",
#     "Branch Name",
#     "Created At"
# ]

# try:

#     creds = Credentials.from_service_account_info(
#         st.secrets["gcp_service_account"],
#         scopes=SCOPES
#     )

#     client = gspread.authorize(creds)

#     SHEET_ID = "1kfoJPOwkIP8lUQcBIZKsjVooVS9MoqRSCXeF4EE5wwk"

#     spreadsheet = client.open_by_key(SHEET_ID)

#     sheet = spreadsheet.sheet1

# except Exception as e:

#     st.error("❌ Google Sheets connection failed")

#     st.exception(e)

#     st.stop()

# # =====================================================
# # CREATE HEADERS
# # =====================================================

# try:

#     existing_data = sheet.get_all_values()

#     if len(existing_data) == 0:

#         sheet.append_row(EXPECTED_HEADERS)

#     elif existing_data[0] != EXPECTED_HEADERS:

#         sheet.resize(rows=1)

#         sheet.update("A1:I1", [EXPECTED_HEADERS])

# except Exception as e:

#     st.error(e)

# # =====================================================
# # FUNCTIONS
# # =====================================================

# def load_df():

#     records = sheet.get_all_records()

#     if not records:

#         return pd.DataFrame(columns=EXPECTED_HEADERS)

#     df = pd.DataFrame(records)

#     if "Date" in df.columns:

#         df["Date_sort"] = pd.to_datetime(
#             df["Date"],
#             errors="coerce"
#         )

#         df = df.sort_values(
#             "Date_sort",
#             ascending=True,
#             na_position="last"
#         )

#         df = df.drop(columns=["Date_sort"])

#     return df


# def append_record(row_data):

#     sheet.append_row(row_data)


# def find_row_by_id(record_id):

#     id_col = sheet.col_values(1)

#     for idx, value in enumerate(id_col[1:], start=2):

#         if value == record_id:

#             return idx

#     return None


# def update_record(record_id, row_data):

#     row_num = find_row_by_id(record_id)

#     if not row_num:

#         return False

#     sheet.update(f"A{row_num}:I{row_num}", [row_data])

#     return True


# def delete_record(record_id):

#     row_num = find_row_by_id(record_id)

#     if not row_num:

#         return False

#     sheet.delete_rows(row_num)

#     return True


# def apply_row_color(row_num, deployed_status):

#     if deployed_status == "On Client":

#         color = {
#             "red": 0.75,
#             "green": 0.95,
#             "blue": 0.75
#         }

#     elif deployed_status == "Server-148":

#         color = {
#             "red": 1.0,
#             "green": 0.90,
#             "blue": 0.60
#         }

#     elif deployed_status == "Server-177":

#         color = {
#             "red": 0.70,
#             "green": 0.85,
#             "blue": 1.0
#         }

#     else:

#         color = {
#             "red": 1.0,
#             "green": 0.70,
#             "blue": 0.70
#         }

#     sheet.format(
#         f"A{row_num}:I{row_num}",
#         {
#             "backgroundColor": color
#         }
#     )

# # =====================================================
# # SESSION STATE
# # =====================================================

# if "edit_mode" not in st.session_state:

#     st.session_state.edit_mode = False

# if "edit_id" not in st.session_state:

#     st.session_state.edit_id = None

# # =====================================================
# # CSS
# # =====================================================

# st.markdown("""
# <style>

# .main-title {
#     font-size: 40px;
#     font-weight: bold;
#     margin-bottom: 10px;
# }

# .sub-title {
#     color: gray;
#     margin-bottom: 30px;
# }

# .stButton > button {
#     width: 100%;
#     border-radius: 10px;
#     height: 42px;
#     font-size: 15px;
#     font-weight: bold;
# }

# </style>
# """, unsafe_allow_html=True)

# # =====================================================
# # HEADER
# # =====================================================

# st.markdown(
#     '<div class="main-title">🚀 Task Tracker</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="sub-title">Track deployments, fixes and customizations</div>',
#     unsafe_allow_html=True
# )

# # =====================================================
# # LOAD DATA
# # =====================================================

# df = load_df()

# # =====================================================
# # DISPLAY TASKS
# # =====================================================

# if not df.empty:

#     st.subheader("📋 Saved Tasks")

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         filter_client = st.text_input(
#             "Search Client"
#         )

#     with col2:

#         filter_category = st.selectbox(
#             "Filter Category",
#             [
#                 "All",
#                 "Hot Fix",
#                 "Bug Fix",
#                 "Customization"
#             ]
#         )

#     with col3:

#         filter_status = st.selectbox(
#             "Filter Deployment",
#             [
#                 "All",
#                 "On Client",
#                 "Server-148",
#                 "Server-177",
#                 "Not Deployed"
#             ]
#         )

#     filtered_df = df.copy()

#     if filter_client:

#         filtered_df = filtered_df[
#             filtered_df["Client"]
#             .astype(str)
#             .str.contains(filter_client, case=False, na=False)
#         ]

#     if filter_category != "All":

#         filtered_df = filtered_df[
#             filtered_df["Category"] == filter_category
#         ]

#     if filter_status != "All":

#         filtered_df = filtered_df[
#             filtered_df["Deployed Status"] == filter_status
#         ]

#     # =================================================
#     # TASK CARDS
#     # =================================================

#     for _, row in filtered_df.iterrows():

#         status = row["Deployed Status"]

#         if status == "On Client":

#             bg = "#d4edda"

#         elif status == "Server-148":

#             bg = "#fff3cd"

#         elif status == "Server-177":

#             bg = "#d1ecf1"

#         else:

#             bg = "#f8d7da"

#         st.markdown(
#             f"""
#             <div style="
#                 background-color:{bg};
#                 padding:18px;
#                 border-radius:15px;
#                 margin-bottom:15px;
#                 border:1px solid #ddd;
#             ">
#             """,
#             unsafe_allow_html=True
#         )

#         col1, col2, col3 = st.columns([8, 1, 1])

#         with col1:

#             st.markdown(f"""
# ### 🏢 {row['Client']}

# **📅 Date:** {row['Date']}

# **📌 Category:** {row['Category']}

# **🚀 Deployment:** {row['Deployed Status']}

# **🌿 Branch:** {row['Branch Name']}

# **📝 Task:**  
# {row['Task Description']}

# **📂 Files:**  
# ```text
# {row['Files List']}
# ```
# """)

#         with col2:

#             if st.button(
#                 "✏️",
#                 key=f"edit_{row['ID']}"
#             ):

#                 st.session_state.edit_mode = True

#                 st.session_state.edit_id = row["ID"]

#                 st.rerun()

#         with col3:

#             if st.button(
#                 "🗑️",
#                 key=f"delete_{row['ID']}"
#             ):

#                 try:

#                     delete_record(row["ID"])

#                     st.success("✅ Record deleted")

#                     st.rerun()

#                 except Exception as e:

#                     st.error("❌ Delete failed")

#                     st.exception(e)

#         st.markdown("</div>", unsafe_allow_html=True)

# # =====================================================
# # ADD / UPDATE SECTION
# # =====================================================

# st.divider()

# if st.session_state.edit_mode:

#     st.subheader("✏️ Update Task")

#     edit_row = df[
#         df["ID"] == st.session_state.edit_id
#     ].iloc[0]

# else:

#     st.subheader("➕ Add New Task")

# # =====================================================
# # DEFAULT VALUES
# # =====================================================

# default_date = datetime.today().date()
# default_client = ""
# default_category = "Hot Fix"
# default_status = "On Client"
# default_branch = ""
# default_task = ""
# default_files = ""

# if st.session_state.edit_mode:

#     default_date = pd.to_datetime(
#         edit_row["Date"]
#     ).date()

#     default_client = str(edit_row["Client"])

#     default_category = str(edit_row["Category"])

#     default_status = str(edit_row["Deployed Status"])

#     default_branch = str(edit_row["Branch Name"])

#     default_task = str(edit_row["Task Description"])

#     default_files = str(edit_row["Files List"])

# # =====================================================
# # FORM
# # =====================================================

# with st.form("task_form", clear_on_submit=False):

#     col1, col2 = st.columns(2)

#     with col1:

#         task_date = st.date_input(
#             "Date",
#             value=default_date
#         )

#         client_name = st.text_input(
#             "Client Name",
#             value=default_client
#         )

#         category = st.selectbox(
#             "Category",
#             ["Hot Fix", "Bug Fix", "Customization"],
#             index=[
#                 "Hot Fix",
#                 "Bug Fix",
#                 "Customization"
#             ].index(default_category)
#         )

#     with col2:

#         deployed_status = st.selectbox(
#             "Deployment Status",
#             [
#                 "On Client",
#                 "Server-148",
#                 "Server-177",
#                 "Not Deployed"
#             ],
#             index=[
#                 "On Client",
#                 "Server-148",
#                 "Server-177",
#                 "Not Deployed"
#             ].index(default_status)
#         )

#         branch_name = st.text_input(
#             "Branch Name",
#             value=default_branch
#         )

#     task_description = st.text_area(
#         "Task Description",
#         value=default_task,
#         height=120
#     )

#     files_list = st.text_area(
#         "Files List",
#         value=default_files,
#         height=120
#     )

#     save_btn = st.form_submit_button(
#         "💾 Save Task"
#     )

# # =====================================================
# # SAVE / UPDATE LOGIC
# # =====================================================

# if save_btn:

#     try:

#         created_at = datetime.now().strftime(
#             "%Y-%m-%d %H:%M:%S"
#         )

#         # =============================================
#         # UPDATE RECORD
#         # =============================================

#         if st.session_state.edit_mode:

#             updated_row = [
#                 st.session_state.edit_id,
#                 str(task_date),
#                 task_description,
#                 files_list,
#                 category,
#                 deployed_status,
#                 client_name,
#                 branch_name,
#                 created_at
#             ]

#             update_record(
#                 st.session_state.edit_id,
#                 updated_row
#             )

#             row_num = find_row_by_id(
#                 st.session_state.edit_id
#             )

#             apply_row_color(
#                 row_num,
#                 deployed_status
#             )

#             st.success("✅ Task updated successfully!")

#             st.session_state.edit_mode = False

#             st.session_state.edit_id = None

#         # =============================================
#         # CREATE RECORD
#         # =============================================

#         else:

#             record_id = str(uuid.uuid4())[:8]

#             new_row = [
#                 record_id,
#                 str(task_date),
#                 task_description,
#                 files_list,
#                 category,
#                 deployed_status,
#                 client_name,
#                 branch_name,
#                 created_at
#             ]

#             append_record(new_row)

#             last_row = len(sheet.get_all_values())

#             apply_row_color(
#                 last_row,
#                 deployed_status
#             )

#             st.success("✅ Task created successfully!")

#         st.rerun()

#     except Exception as e:

#         st.error("❌ Operation failed")

#         st.exception(e)


#new updated:
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import uuid

st.set_page_config(page_title="Task Tracker", page_icon="🚀", layout="wide")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

EXPECTED_HEADERS = [
    "ID",
    "Date",
    "Task Description",
    "Files List",
    "Category",
    "Deployed Status",
    "Client",
    "Branch Name",
    "Created At"
]

# =========================================================
# GOOGLE SHEETS CONNECTION
# =========================================================

try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    SHEET_ID = "1kfoJPOwkIP8lUQcBIZKsjVooVS9MoqRSCXeF4EE5wwk"

    spreadsheet = client.open_by_key(SHEET_ID)

    sheet = spreadsheet.sheet1

except Exception as e:

    st.error("❌ Google Sheets connection failed")
    st.exception(e)
    st.stop()

# =========================================================
# VALIDATE SHEET HEADERS
# =========================================================

try:

    existing_data = sheet.get_all_values()

    if len(existing_data) == 0:

        sheet.append_row(EXPECTED_HEADERS)

    elif existing_data[0] != EXPECTED_HEADERS:

        sheet.resize(rows=1)

        sheet.update("A1:I1", [EXPECTED_HEADERS])

except Exception as e:

    st.error(e)

# =========================================================
# FUNCTIONS
# =========================================================

def load_df():

    records = sheet.get_all_records()

    if not records:
        return pd.DataFrame(columns=EXPECTED_HEADERS)

    df = pd.DataFrame(records)

    if "Date" in df.columns:

        df["Date_sort"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        df = df.sort_values(
            "Date_sort",
            ascending=False,
            na_position="last"
        )

        df = df.drop(columns=["Date_sort"])

    return df


def append_record(row_data):

    sheet.append_row(row_data)


def find_row_by_id(record_id):

    id_col = sheet.col_values(1)

    for idx, value in enumerate(id_col[1:], start=2):

        if value == record_id:
            return idx

    return None


def update_record(record_id, row_data):

    row_num = find_row_by_id(record_id)

    if not row_num:
        return False

    sheet.update(f"A{row_num}:I{row_num}", [row_data])

    return True


def delete_record(record_id):

    row_num = find_row_by_id(record_id)

    if not row_num:
        return False

    sheet.delete_rows(row_num)

    return True

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 10px;
}

.sub-title {
    color: gray;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚀 Task Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Track deployments, fixes and customizations</div>',
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

df = load_df()

# =========================================================
# 1. ADD NEW TASK
# =========================================================

st.subheader("➕ Add New Task")

with st.form("deployment_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:

        task_date = st.date_input(
            "Date",
            value=datetime.today().date()
        )

        client_name = st.text_input(
            "Client Name",
            placeholder="Enter client name"
        )

        category = st.selectbox(
            "Category",
            ["Hot Fix", "Bug Fix", "Customization"]
        )

    with col2:

        deployed_status = st.selectbox(
            "Deployment Status",
            ["On Client", "Server-148", "Server-177", "Not Deployed"]
        )

        branch_name = st.text_input(
            "Branch Name",
            placeholder="feature/report-cleanup"
        )

    task_description = st.text_area(
        "Task Description",
        placeholder="Explain the task...",
        height=120
    )

    files_list = st.text_area(
        "Files List",
        placeholder="""Controllers/ReportController.cs
Services/ReportService.cs
Views/Report/Index.cshtml""",
        height=120
    )

    submitted = st.form_submit_button("Save Task")

# =========================================================
# SAVE TASK
# =========================================================

if submitted:

    if task_description.strip() == "":

        st.error("Task Description is required")

    else:

        try:

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            record_id = str(uuid.uuid4())

            row = [
                record_id,
                str(task_date),
                task_description,
                files_list,
                category,
                deployed_status,
                client_name,
                branch_name,
                created_at
            ]

            append_record(row)

            st.success("✅ Task saved successfully!")

            st.rerun()

        except Exception as e:

            st.error("❌ Failed to save task")
            st.exception(e)

# =========================================================
# 2. SAVED TASKS
# =========================================================

st.divider()

filtered_df = df.copy()

if not df.empty:

    st.subheader("📋 Saved Tasks")

    f1, f2, f3, f4 = st.columns(4)

    # =====================================================
    # SEARCH CLIENT
    # =====================================================

    with f1:

        filter_client = st.text_input(
            "Search Client"
        )

    # =====================================================
    # FILTER DATE
    # =====================================================

    with f2:

        filter_date = st.date_input(
            "Filter Date",
            value=None
        )

    # =====================================================
    # FILTER CATEGORY
    # =====================================================

    with f3:

        filter_category = st.selectbox(
            "Category",
            ["All", "Hot Fix", "Bug Fix", "Customization"]
        )

    # =====================================================
    # FILTER STATUS
    # =====================================================

    with f4:

        filter_status = st.selectbox(
            "Deployment Status",
            ["All", "On Client", "Server-148", "Server-177", "Not Deployed"]
        )

    # =====================================================
    # APPLY FILTERS
    # =====================================================

    if filter_client:

        filtered_df = filtered_df[
            filtered_df["Client"]
            .astype(str)
            .str.contains(filter_client, case=False, na=False)
        ]

    if filter_date:

        filtered_df = filtered_df[
            pd.to_datetime(
                filtered_df["Date"]
            ).dt.date == filter_date
        ]

    if filter_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] == filter_category
        ]

    if filter_status != "All":

        filtered_df = filtered_df[
            filtered_df["Deployed Status"] == filter_status
        ]

    # =====================================================
    # SHOW TABLE
    # =====================================================

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

# =========================================================
# 3. UPDATE / DELETE TASK
# =========================================================

st.divider()

if not df.empty:

    st.subheader("✏️ Edit or Delete Record")

    # =====================================================
    # SEARCH BY ID
    # =====================================================

    search_id = st.text_input(
        "Search Task By ID",
        placeholder="Paste task ID here..."
    )

    selected_row = None

    if search_id:

        matching_rows = filtered_df[
            filtered_df["ID"]
            .astype(str)
            .str.contains(search_id.strip(), case=False, na=False)
        ]

        if not matching_rows.empty:

            selected_row = matching_rows.iloc[0]

            st.success("✅ Task Found")

        else:

            st.warning("No task found with this ID")

    # =====================================================
    # SHOW EDIT FORM
    # =====================================================

    if selected_row is not None:

        with st.form("edit_form"):

            c1, c2 = st.columns(2)

            # =================================================
            # LEFT SIDE
            # =================================================

            with c1:

                edit_date = st.date_input(
                    "Date",
                    value=pd.to_datetime(
                        selected_row["Date"]
                    ).date()
                )

                edit_client = st.text_input(
                    "Client Name",
                    value=str(selected_row["Client"])
                )

                edit_category = st.selectbox(
                    "Category",
                    ["Hot Fix", "Bug Fix", "Customization"],
                    index=[
                        "Hot Fix",
                        "Bug Fix",
                        "Customization"
                    ].index(
                        str(selected_row["Category"])
                    )
                )

            # =================================================
            # RIGHT SIDE
            # =================================================

            with c2:

                edit_status = st.selectbox(
                    "Deployment Status",
                    ["On Client", "Server-148", "Server-177", "Not Deployed"],
                    index=[
                        "On Client",
                        "Server-148",
                        "Server-177",
                        "Not Deployed"
                    ].index(
                        str(selected_row["Deployed Status"])
                    )
                )

                edit_branch = st.text_input(
                    "Branch Name",
                    value=str(selected_row["Branch Name"])
                )

            # =================================================
            # TEXT AREAS
            # =================================================

            edit_task = st.text_area(
                "Task Description",
                value=str(selected_row["Task Description"]),
                height=120
            )

            edit_files = st.text_area(
                "Files List",
                value=str(selected_row["Files List"]),
                height=120
            )

            # =================================================
            # BUTTONS
            # =================================================

            save_edit = st.form_submit_button(
                "Update Record"
            )

            delete_btn = st.form_submit_button(
                "Delete Record"
            )

        # =====================================================
        # UPDATE RECORD
        # =====================================================

        if save_edit:

            try:

                selected_id = str(selected_row["ID"])

                updated_row = [
                    selected_id,
                    str(edit_date),
                    edit_task,
                    edit_files,
                    edit_category,
                    edit_status,
                    edit_client,
                    edit_branch,
                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                ]

                if update_record(selected_id, updated_row):

                    st.success("✅ Record updated successfully!")

                    st.rerun()

                else:

                    st.error("Record not found")

            except Exception as e:

                st.error("❌ Failed to update record")
                st.exception(e)

        # =====================================================
        # DELETE RECORD
        # =====================================================

        if delete_btn:

            try:

                selected_id = str(selected_row["ID"])

                if delete_record(selected_id):

                    st.success("🗑️ Record deleted successfully!")

                    st.rerun()

                else:

                    st.error("Record not found")

            except Exception as e:

                st.error("❌ Failed to delete record")
                st.exception(e)