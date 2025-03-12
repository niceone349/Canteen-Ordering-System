import streamlit as st
import os
import base64

st.set_page_config(page_title="Stores", page_icon="🏪", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/StoresStudent.png")
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
    background-color: rgba(0, 0, 0, 0.4); 
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
label, input, h1, h5, h6, hr, textarea, sidebar, select{{
    color: white !important;
}}
div[data-testid="stTextInput"] input {{
    background-color: #262730 !important; 
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
        div[data-testid="stSidebarNav"] { display: none !important; }
        .stButton > button {
            width: 100%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;background-color: rgba(19, 23, 32, 1);
            color: white !important; 

        }
        .stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.3) !important; 
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
        section[data-testid="stSidebar"] { visibility: visible !important; }
    </style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")

Student_Name = st.session_state.get("store_name", "")


st.sidebar.title(f"Hi! {Student_Name}")

st.sidebar.page_link("pages/Student_Home.py", label="Home")
st.sidebar.page_link("pages/Student_Stores.py", label="Stores")

st.markdown(f"<h1 style='text-align: center;'>Welcome, {Student_Name}!</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

Store = {}
if os.path.exists("users.txt"):
    with open("users.txt", "r") as file:
        for line in file:
            values = line.strip().split(",")
            if len(values) == 4 and values[3] == "admin":
                username, password, store_name = values[:3]
                Store[store_name] = username  

st.markdown("<h6>Select a Store:</h6>", unsafe_allow_html=True)
for Store in Store.keys():
    if st.button(Store):
        st.session_state["selected_store"] = Store
        st.switch_page("pages/Student_Menu.py")
                       

def logout():
    st.session_state["logged_in"] = False
    st.session_state("selected_store", None)
    st.rerun()
