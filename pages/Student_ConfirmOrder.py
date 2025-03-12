import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time
import base64

st.set_page_config(page_title="Order Confirmation", page_icon="✅", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/ConfirmStudent.png")
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
    background-color: rgba(0, 0, 0, 0.6); 
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
label, input, table, thead th, tbody tr th,  h1, h2, h3, h5, h6, hr, textarea, sidebar, select{{
    color: white !important;
}}
div[data-testid="stTextInput"] input {{
    background-color: #262730 !important; 
}}
section[data-testid="stSidebar"] *{{
    color: white !important;
}}
div[data-testid="stCheckbox"] label *{{
    color: white !important;
}}
details div {{
    color: white !important;
}}

div[data-testid="stFileUploader"] section {{
    background-color: rgb(38, 39, 48) !important; 

}}
div[data-testid="stFileUploader"] * {{
    color: white !important;
}}
div[data-testid="stFileUploader"] button {{
    background-color: #131720 !important;
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
            width: 100%;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            background-color: rgba(19, 23, 32, 1);
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


st.title("Confirm Order")

if "selected_store" not in st.session_state:
    st.warning("No store selected. Please go back and select a store.")
    st.stop()

if "username" not in st.session_state:
    st.warning("No username found. Please log in again.")
    st.stop()

if "order_summary" not in st.session_state or not st.session_state["order_summary"]:
    st.warning("No order details found. Please go back and place an order.")
    st.stop()

store_name = st.session_state["selected_store"]
student_name = st.session_state["username"]
discount_name = st.session_state.get("discount_name", "")
order_summary = st.session_state["order_summary"]
discount_applied = st.session_state.get("discount_applied", 0)
discount_container = st.session_state.get("discount_container")
final_price = st.session_state.get("final_price", 0)

order_data = [
    {"Item Name": item, "Quantity": qty, "Price (₱)": f"{price:.2f}", "Total (₱)": f"{qty * price:.2f}"}
    for item, (qty, price) in order_summary.items()
]

st.markdown("<h3>Order Summary</h3>", unsafe_allow_html=True)
st.table(pd.DataFrame(order_data))

if discount_applied > 0:
    st.markdown(f"**Discount Applied:** -₱{discount_applied:.2f}")
    if discount_container:
        st.markdown(f"**Container Discount applied: -10%**")
st.markdown(f"### **Total Price: ₱{final_price:.2f}**")

qr_payments = {}
if os.path.exists("payments.txt"):
    with open("payments.txt", "r") as file:
        for line in file:
            values = line.strip().split(",")
            if len(values) == 2:
                qr_payments[values[0]] = values[1]

if store_name in qr_payments and os.path.exists(qr_payments[store_name]):
    st.image(get_base64_image(qr_payments[store_name]), width=350, )
    st.markdown(
    "<p style='color: grey;'>Scan this QR to pay</p>",
    unsafe_allow_html=True
)
else:
    st.error("No QR payment image found for this store.")

st.markdown("<h6>Please present the proof of payment upon pick up</h6>", unsafe_allow_html=True)

st.markdown("### **Upload Proof of Payment**")

uploaded_file = st.file_uploader("Upload your payment proof (JPG/PNG)", type=["jpg", "png"])


col1, col2 = st.columns(2)

with col1:
    if st.button("Go Back"):
        st.switch_page("pages/Student_Menu.py")

with col2:
    if st.button("Confirm Order"):
        menu_file = "samplemenu.txt"
        discount_file = "discounts.txt"
        if uploaded_file:
            UPLOAD_FOLDER = "proof_of_payments"
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{store_name}_{student_name}_{timestamp}.png"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with open("proof_of_payments.txt", "a") as file:
                file.write(f"{store_name},{student_name},{file_path}\n")
            
            st.session_state["proof_of_payment_path"] = file_path  
            
            if os.path.exists(menu_file):
                updated_menu = []
                with open(menu_file, "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 6 and values[0] == store_name:
                            _, item, description, price, stock, availability = values
                            stock = int(stock)
                            
                            if item in order_summary:
                                qty_ordered, _ = order_summary[item]
                                stock -= qty_ordered
                                availability = "Out of stock" if stock == 0 else "Available"

                            updated_menu.append(f"{store_name},{item},{description},{price},{stock},{availability}\n")
                        else:
                            updated_menu.append(line)
                
                with open(menu_file, "w") as file:
                    file.writelines(updated_menu)

            if discount_applied > 0 and os.path.exists(discount_file):
                updated_discounts = []
                with open(discount_file, "r") as file:
                    for line in file:
                        values = line.strip().split(",")
                        if len(values) == 4 and values[0] == store_name and values[1] == discount_name:
                            continue 
                        updated_discounts.append(line)

                with open(discount_file, "w") as file:
                    file.writelines(updated_discounts)

            st.success("Order confirmed successfully!")
            time.sleep(2)
            st.switch_page("pages/Student_Stores.py")
        else:
            st.warning("Please Upload Proof of Payment!")

