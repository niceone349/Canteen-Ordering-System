import streamlit as st
import os
import base64

st.set_page_config(page_title="Login", page_icon="🔑", layout="wide")


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/MAPUA.png")

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
    background-color: rgba(0, 0, 0, 0.4); 
    z-index: 0;
}}

/* Input Field Container */
div[data-testid="stForm"] {{
    background: rgba(14, 17, 23, 0.8) !important; 
    padding: 20px !important;
    border-radius: 10px !important;
    color: rgba(255,255,255, 1)
}}

label, input,h2, textarea, select{{
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
div[data-testid="stForm"] button {{
    background-color: #262730 !important;
    color: white !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;} 
        div[data-testid="stDataFrame"] td { 
            white-space: normal !important; 
            word-break: break-word !important;
            overflow-wrap: break-word !important;
        }
        div[data-testid="stDataFrameContainer"] {
            width: 100% !important;
        }
        /* Hide the first sidebar navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
        .stButton > button {
            width: 100% !important;
            height: 70px !important;
            font-size: 20px !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            display: block !important;
            background-color: rgba(19, 23, 32, 1);
            color: white !important;
        }
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100% !important;
        }
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        [data-testid="stSidebar"] {
            visibility: hidden;
            width: 0px;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    <script>
        window.onload = function() {
            var sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.visibility = 'hidden';
                sidebar.style.width = '0px';
            }
        }
    </script>
""", unsafe_allow_html=True)


users_file = "users.txt"

if not os.path.exists(users_file):
    st.error("Database not found.")

def check_user(username, password):
    with open(users_file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            if username == values[0] and password == values[1]:
                return values[2], values[3]
    return None, None

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "store_name" not in st.session_state:
    st.session_state["store_name"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
    
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["store_name"] = None
    st.session_state["role"] = None
    st.rerun()


if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔒Login</h2>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username/User ID")
        password = st.text_input("🔑 Password", type="password")
        if st.form_submit_button("Login"):
            store_name, role = check_user(username, password)
            if store_name:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["store_name"] = store_name 
                st.session_state["role"] = role 
                st.success(f"Welcome, {store_name}! Redirecting...")
                if role == "admin":
                    st.switch_page("pages/1_Home.py")
                else:
                    st.switch_page("pages/Student_Home.py")
            else:
                st.error("Invalid Username or Password")


