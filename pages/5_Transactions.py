import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64
st.set_page_config(page_title="Transactions", page_icon="🧾", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/TransactionAdmin.png")
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
label, input, h1, h5, hr, textarea, sidebar, select{{
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
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
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
            height: 40px !important;
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
        /* Ensure only the custom sidebar is visible */
        section[data-testid="stSidebar"] {
            visibility: visible !important;
        }
    </style>
""", unsafe_allow_html=True)

user_role = st.session_state.get("role", "") 
store_name = st.session_state.get("store_name", "")

st.sidebar.title(f"{store_name}")

if user_role == "admin":
    st.sidebar.page_link("pages/1_Home.py", label="Home")
    st.sidebar.page_link("pages/2_Menu.py", label="Menu")
    st.sidebar.page_link("pages/3_Discounts.py", label="Discounts")
    st.sidebar.page_link("pages/4_Stock Management.py", label="Stock Management")
    st.sidebar.page_link("pages/5_Transactions.py", label="Transactions")
    
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("Login.py")


st.markdown(f"<h1 style='text-align: center;'>{store_name} Transactions</h1>", unsafe_allow_html=True)

lines = []
with open("proof_of_payments.txt", "r") as file:
    for line in file:
        values = line.strip().split(",")
        if len(values) == 3 and values[0] == store_name:
            lines.append([values[1], values[2]])

df = pd.DataFrame(lines, columns=["Student ID", "Proof of Payment"])
if lines:
    if "visible_images" not in st.session_state:
        st.session_state["visible_images"] = {}

    def toggle_image(index, image_path):
        if index in st.session_state["visible_images"]:
            del st.session_state["visible_images"][index]
        else:
            st.session_state["visible_images"][index] = image_path

    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([2, 6, 2])
        col1.write(row["Student ID"])
        col2.write(row["Proof of Payment"])
        if col3.button("View Image", key=f"btn_{index}"):
            toggle_image(index, row["Proof of Payment"])
        
        if index in st.session_state["visible_images"]:
            image_path = st.session_state["visible_images"][index]
            if os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption="Proof of Payment", use_container_width=True)
            else:
                st.error("Image not found.")
else:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center;'>No Transactions Available.</h5>", unsafe_allow_html=True)