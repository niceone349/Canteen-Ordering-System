import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Menu", page_icon="📜", layout="wide")


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("design/MenuAdmin.png")
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
    background-color: rgba(0, 0, 0, 0.5); 
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
div[data-testid="stExpander"] *{{
    background: rgba(14, 17, 23, 0.8) !important; 
    border-radius: 10px !important;
    color: white !important;
}}
label, input, h1, textarea, sidebar, select{{
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
            background-color: red !important;
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


st.markdown(f"<h1 style='text-align: center;'>{store_name} Menu</h1>", unsafe_allow_html=True)




def add_item():
    with st.expander("Add Item", expanded=False):
        st.write("Fill in the details below:")

        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        price = st.number_input("Price", min_value=0, step=1)

        if st.button("Add Item"):
            if not item_name or not description or price <= 0:
                st.error("Please fill in all fields correctly before submitting.")
                return

            item_exists = False
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 6 and values[1] == item_name:
                        item_exists = True
                        break  

            if item_exists:
                st.error(f"Item '{item_name}' already exists!")
            else:
                with open("samplemenu.txt", "a") as file:
                    file.write(f"{store_name},{item_name},{description},{price} php,0,Out of Stock\n")

                st.success(f"Item '{item_name}' added successfully!")
                st.rerun()  


def update_item():
    with st.expander("Update Item", expanded=False):
        st.write("Select or search for an item to update.")

        lines = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 6 and values[0] == store_name:  
                    lines.append(values)

        if not lines:
            st.warning("No items available to update.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Item Name", "Description", "Price", "Stock", "Status"])

        search_query = st.text_input("Search Item")
        if search_query:
            df = df[df["Item Name"].str.contains(search_query, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to update", df["Item Name"].tolist())

        item_details = df[df["Item Name"] == selected_item].iloc[0]
        current_item_name = item_details["Item Name"]
        current_description = item_details["Description"]
        current_price = item_details["Price"].replace(" php", "")
        stock = item_details["Stock"]
        status = item_details["Status"]

        new_item_name = st.text_input("Item Name", value=current_item_name)  
        new_description = st.text_area("Description", value=current_description)
        new_price = st.number_input("Price", min_value=0, step=1, value=int(current_price))

        if st.button("Update Item"):
            updated_lines = []
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 6 and values[0] == store_name and values[1] == current_item_name:
                        updated_lines.append(f"{store_name},{new_item_name},{new_description},{new_price} php,{stock},{status}\n")
                    else:
                        updated_lines.append(line)

            with open("samplemenu.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"Item '{current_item_name}' updated to '{new_item_name}' successfully!")
            st.rerun()  


def delete_item():
    with st.expander("Delete Item", expanded=False):
        st.write("Search and select an item to delete.")

        lines = []
        with open("samplemenu.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 6 and values[0] == store_name:  
                    lines.append(values)

        if not lines:
            st.warning("No items available to delete.")
            return

        df = pd.DataFrame(lines, columns=["Store", "Item Name", "Description", "Price", "Stock", "Status"])

        search_query_delete = st.text_input("Search Item", key="delete_search")

        if search_query_delete:
            df = df[df["Item Name"].str.contains(search_query_delete, case=False, na=False)]

        if df.empty:
            st.warning("No matching items found.")
            return

        selected_item = st.selectbox("Select an item to delete", df["Item Name"].tolist(), key="delete_select")

        item_details = df[df["Item Name"] == selected_item].iloc[0]
        item_name = item_details["Item Name"]
        item_description = item_details["Description"]
        item_price = item_details["Price"]

        st.markdown(f"**Item Name:** {item_name}")
        st.markdown(f"**Description:** {item_description}")
        st.markdown(f"**Price:** {item_price}")

        if st.button("Confirm Delete", key="delete_button"):
            updated_lines = []
            with open("samplemenu.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 6 and values[0] == store_name and values[1] == item_name:
                        continue  
                    updated_lines.append(line)

            with open("samplemenu.txt", "w") as file:
                file.writelines(updated_lines)

            st.success(f"Item '{item_name}' deleted successfully!")
            st.rerun()  


col1, col2, col3 = st.columns([2, 2, 2])

with col1: 
    add_item()
    
with col2: 
    update_item()
    
with col3: 
    delete_item()


lines = []
with open("samplemenu.txt", "r") as file:
    for line in file:
        values = line.strip().split(",")
        if len(values) == 6 and values[0] == store_name:
            lines.append([values[1], values[2], values[3]])  

df = pd.DataFrame(lines, columns=["Item Name", "Description", "Price"])


st.data_editor(df, 
    use_container_width=True, 
    hide_index=True, 
    column_config={
        "Description": st.column_config.TextColumn(width="large", help="Full description visible")
    }
)
