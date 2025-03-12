import streamlit as st
import base64

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/HomeStudent.png")
sidebar_base64 = get_base64_image("design/Sidebar.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    position: absolute;
    background-image: url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
}}

[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3); 
    z-index: 0;
}}

[data-testid="stHeader"]{{
background-color: rgba(0, 0, 0, 0);
}}
[data-testid="stSidebar"]{{
    position: absolute;
    background-image: url("data:image/jpg;base64,{sidebar_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center
}}
[data-testid="stSidebar"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3); 
    z-index: 0;
}}
div[data-testid="stExpander"] {{
    background: rgba(14, 17, 23, 0.8) !important; 
    border-radius: 10px !important;
}}

label, input, textarea, h1, h5, hr, sidebar, select{{
    color: white !important;
}}
div[data-testid="stTextInput"] input {{
    background-color: #262730 !important; 
}}
div[data-testid="stTextInput"] button {{
    background-color: #262730 !important;
    color: white !important; 
}}
div[data-testid="stTextInput"] > div {{
    background-color: #262730 !important;  
    border: none !important;
}}
section[data-testid="stSidebar"] *{{
    color: white !important;
}}

details div {{
    color: white !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("""
    <style>
        /* Hide the first sidebar navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            background-color: rgba(19, 23, 32, 1);
            color: white !important; 
        }
        .stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.5) !important; 
            color: white !important; 
            border: 2px solid rgba(255, 255, 255, 0.3) !important; 
        }
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100% !important;
        }
        /* Ensure only the custom sidebar is visible */
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }
    </style>
""", unsafe_allow_html=True)

user_role = st.session_state.get("role", "") 
Student_Name = st.session_state["store_name"]

st.sidebar.title(f"Hi! {Student_Name}")

if user_role == "student":
    st.sidebar.page_link("pages/Student_Home.py", label="Home")
    st.sidebar.page_link("pages/Student_Stores.py", label="Stores")
else:
    st.sidebar.write("Please log in to see pages.")
    

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")
if "edit_expanded" not in st.session_state:
    st.session_state["edit_expanded"] = False
def logout():
    st.session_state["logged_in"] = False
    st.rerun()
    
st.markdown(f"<h1 style='text-align: center;'>Welcome! {Student_Name}.</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


if st.button("Edit Account Details"):
    st.session_state["edit_expanded"] = not st.session_state["edit_expanded"] 


if st.session_state["edit_expanded"]:
    with st.expander("Edit Account Details", expanded=True):
        st.write("Update your account details below:")

        current_username = st.session_state.get("username", "")
        st.markdown(f"**Student Number: {current_username}**")
        new_password = st.text_input("New Password", type="password", key="new_password")

        if st.button("Update", key="update_btn"):
            if new_password:
                updated_lines = []
                with open("users.txt", "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 4 and values[0] == current_username:
                            updated_lines.append(f"{values[0]},{new_password},{values[2]},{values[3]}\n")
                        else:
                            updated_lines.append(line)

                with open("users.txt", "w") as file:
                    file.writelines(updated_lines)

                st.session_state["username"] = current_username
                st.success("Account details updated successfully!")
                
            else:
                st.error("Please fill in required fields before updating.")


if st.button("Logout"):
    logout()