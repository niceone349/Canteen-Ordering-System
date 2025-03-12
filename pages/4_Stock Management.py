import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Stock Management", page_icon="📃", layout="wide")


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/StockAdmin.png")
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
    background-color: rgba(0,0,0, 0.6); 
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
label, input, h1, textarea, sidebar, select{{
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



st.markdown(f"<h1 style='text-align: center;'>{store_name} Stock Management</h1>", unsafe_allow_html=True)



def update_stock():
    with st.expander("Update Stock", expanded=False):
        st.write("Select or search for a stock item to update.")


        items = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 6 and values[0] == store_name:  
                    items.append(values)

        if not items:
            st.warning("No items available to update.")
            return

        df = pd.DataFrame(items, columns=["Store", "Item Name", "Description", "Price", "Stock", "Status"])


        search_query = st.text_input("Search Stock")
        if search_query:
            df = df[df["Item Name"].str.contains(search_query, case=False, na=False)]

        if df.empty:
            st.warning("No matching stocks found.")
            return


        selected_item = st.selectbox("Select a Stock to update", df["Item Name"].tolist())


        item_details = df[df["Item Name"] == selected_item].iloc[0]
        current_stock_name = item_details["Item Name"]
        current_stock = item_details["Stock"]

        new_stock = st.number_input("New Stock Quantity", min_value=0, step=1, value=int(current_stock))


        if st.button("Update Stock"):
            if(new_stock <= 0):
                new_status = "Out of Stock"
            else:
                new_status = "Available"
                
            updated_lines = []
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 6 and values[0] == store_name and values[1] == current_stock_name:
                        updated_lines.append(f"{store_name},{values[1]},{values[2]},{values[3]},{new_stock},{new_status}\n")
                    else:
                        updated_lines.append(line)


            with open("samplemenu.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"Stock and status for '{current_stock_name}' updated successfully!")
            st.rerun()  


update_stock()


items = []
with open("samplemenu.txt", "r") as file:
    for line in file:
        values = line.strip().split(",")
        if len(values) == 6 and values[0] == store_name:
            items.append([values[1], values[4], values[5]])  

df = pd.DataFrame(items, columns=["Item Name", "Stock", "Status"])


st.data_editor(df, 
    use_container_width=True, 
    hide_index=True, 
    column_config={
        "Stock": st.column_config.NumberColumn(help="Available stock quantity"),
        "Status": st.column_config.TextColumn(help="Current stock status")
    }
)
