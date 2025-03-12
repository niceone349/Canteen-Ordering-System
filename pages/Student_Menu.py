import streamlit as st
import os
import base64
st.set_page_config(page_title="Menu", page_icon="📜", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/MenuStudent.png")
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
    background-color: rgba(255,255,255, 0.1); 
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
    background: rgba(14, 17, 23, 0.9) !important; 
    border-radius: 10px !important;
}}
label, input, h1, h2, h5, hr, textarea, sidebar, select{{
    color: white !important;
}}
div[data-testid="stTextInput"] input {{
    background-color: #262730 !important; 
}}
div[data-testid="stNumberInput"] input {{
    background-color: #262730 !important; 
}}
div[data-testid="stNumberInput"] button {{
    background-color: #262730 !important;
    color: white !important;
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

store_name = st.session_state["selected_store"]

st.title(f"{store_name} Menu")

if os.path.exists("samplemenu.txt"):
        menu_items = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 6 and values[0] == store_name:
                    _, item, description, price, stock, availability = values
                    menu_items.append({
                        "name": item,
                        "description": description,
                        "price": float(price.split()[0]), 
                        "stock": int(stock),
                        "available": availability.lower() == "available"
                    })

        if menu_items:
            col1, col2= st.columns([3, 1])

            with col1: 

                with st.expander(f"{store_name} Menu", expanded=True):
                    st.markdown("Select Items to Order:")
                    order = {}
                    for item in menu_items:
                        if item["available"]:
                            quantity = st.number_input(
                                f"**{item['name']}** - {item['description']} (₱{item['price']:.2f})",
                                min_value=0, max_value=item["stock"], value=0, step=1
                            )
                            if quantity > 0:
                                order[item["name"]] = (quantity, item["price"])

                    total_price = sum(qty * price for qty, price in order.values())
            with col2:
                    discount = 0.00
                    discount_found = False
                    discount_name = st.text_input("Discount Vouchers")
                    discount_container = st.checkbox("Bring your own container discount")
                    
                    if os.path.exists("discounts.txt"):
                        with open("discounts.txt", "r") as file:
                            discount_lines = file.readlines()

                        for line in discount_lines:
                            values = line.strip().split(",")
                            if len(values) == 4 and values[0] == store_name and values[1] == discount_name:
                                discount = float(values[2].split(' ')[0])
                                discount_found = True
                                break
                            elif discount_name == "":
                                discount_found = True
                                break
                    if discount_container:
                        final_price = (total_price * 0.90) - discount
                    else:
                        final_price = total_price - discount          
                    
                    st.markdown(f"<h2 style='font-size: 20px;'>Total: <b>₱{final_price:.2f}</b></h2>", unsafe_allow_html=True)

                    if discount > 0:
                        st.markdown(f"*(Discount applied: -₱{discount:.2f})*")
                        if discount_container:
                            st.markdown(f"*(Container Discount applied: -10%)*")
                    elif discount_name and not discount_found:
                        st.warning("Invalid discount voucher.")
                        
                    if st.button("Place Order"):
                        st.session_state["order_summary"] = order
                        st.session_state["discount_applied"] = discount
                        st.session_state["discount_name"] = discount_name
                        st.session_state["discount_container"] = discount_container
                        st.session_state["final_price"] = final_price
                        if discount_found:
                            st.switch_page("pages/Student_ConfirmOrder.py")
                        st.rerun() 
                            
        else:
            st.warning(f"No menu items found for {store_name}.")
        
            
if st.button("Back"):
    st.switch_page("pages/Student_Stores.py")
        