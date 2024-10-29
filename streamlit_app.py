import pandas as pd
import streamlit as st

from data_processing import getBasePrice, getHWPrice
from utils import update_table, update_table_by_key

# custom page icon and page title in tab bar
st.set_page_config(
    page_title="AWMA configurator",
    page_icon="🖥️",
    # initial_sidebar_state="collapsed"
)

# type face
with open("styles.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Insert logo at the top of the page
logo_png = "Erntec_Pos_RGB.png"
with st.columns(3)[1]:
    st.image(logo_png)

# Add notes inside the side bar
with st.sidebar.container():
        st.markdown('<p class="verdana-large">Notes:</p>', unsafe_allow_html=True)
        st.write("""<div class="sidebar-container">
                - Standard PAFD cost = size cost + standard hardware costs<br><br>
                - Any request outside the standard sizes and/or hardware is considered custom & requires a custom price from ERNTEC<br><br>
                - Standard hardware height is 1000mm from FFL<br><br>
                - Standard flood protection height is 900mm from FFL<br><br>
                - Standard sizes are based on australian standard door sizes<br><br>
                - Current costs do not include: <br>
                    <p style="text-indent: 30px;">
                    - Profile or seal as these are free issued by AWMA<br></p>
                    <p style="text-indent: 30px;">
                    - Variation for Colour & Freight</p>""", unsafe_allow_html=True)

###
df = pd.read_csv('SQL_Base.csv')
df1 = pd.read_csv('SQL_HardWare.csv')

st.markdown('<p class="verdana-title">AWMA configurator</p>', unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

columns=['DoorSizeID', 'Mortice', "Latch Plate", "Custom Latch Block",
    "Exterior Plate/Handle (Optional)",
    "Interior Plate/Handle",
    "Additional Hardware (Optional)"]
initial_rows = 1

### Base
st.write("Step 1: Select type of door and size")
col1, col2 = st.columns(2)

door_prices = getBasePrice(df)
with col1:
    door_type = st.radio("Select Door Type:", ["Standard", "Fully Sealed"], horizontal = True)  
with col2:
    door_size = st.selectbox("Select Door Size:", list(door_prices.keys()))

doorprice = door_prices[door_size][door_type]
# st.write(f"DoorSizeID: {doorprice['id']}")
input_door = doorprice['id']

#st.write(f"Price for {door_type} door in {door_size}: ${doorprice['price']:.2f}")

st.divider()

st.write("Step 2: Select Hinge Type")
hinge_type = st.radio("Select:", ["Left hinge", "Right hinge"], horizontal = True)

st.divider()

# HW
st.write("Step 3: Select hardware required")

mandatory_flags = {}
# currently hard-coded because there are no 'mandatory' labels in dataset
mandatory_categories = ["Mortice", "Interior Plate/Handle", "Latch Plate", "Custom Latch Block"]

latch_to_latch_block = {
    "Standard": {
        "Standard Erntec Latch": "No Block Required",
        "Striker, Electric, 12-30Vdc, 25Kg Pre-Load, Multi-Function, No-Lip": "Block, Electric Latch, Machined, Dwg 853-541"
    },
    "Fully Sealed": {
        "Standard Erntec Latch FS": "Block, Standard Latch FS, Machined, Dwg 853-471",
        "Striker, Electric, 12-30Vdc, 25Kg Pre-Load, Multi-Function, No-Lip": "Block, Electric Latch FS, Machined, Dwg 853-555"
    }
}

if door_type in door_prices[door_size]:
    # Retrieve filtered dataset based on door type
    HW_prices = getHWPrice(df1, door_type)
    total_price = doorprice['price']

    ordered_categories = [
    "Mortice",
    "Latch Plate",
    "Exterior Plate/Handle (Optional)",
    "Interior Plate/Handle",
    "Additional Hardware (Optional)"
    ]

    selected_latch = None
    hwid = {}
    for category in ordered_categories:
        if category not in HW_prices:
            continue

        # create selection box for each category
        selected_item = st.selectbox(f"Select {category}:", list(HW_prices[category].keys()), index = None,
                                     placeholder="Select an option...")

        
        # update mandatory field flag
        if category in mandatory_categories:
            category_dict = HW_prices.get(category, {})
            price = category_dict.get(selected_item, 0)
            mandatory_flags[category] = price != 0
        # append price
        if selected_item != None:
            category_dict = HW_prices.get(category, {})
            price = category_dict.get(selected_item, 0)

            total_price += price['price']
            # st.write(f"HardwareID: {price['id']}")

            if category not in hwid:
                hwid[category] = []

            if price['id']:  # Only append if the ID is not None
                hwid[category].append(price['id'])


        if category == "Latch Plate":
            selected_latch = selected_item

            if selected_latch in latch_to_latch_block[door_type]:
                # Get the paired latch block based on the door type
                paired_block = latch_to_latch_block[door_type][selected_latch]
                
                st.selectbox("Paired Latch Block:", [paired_block])
                
                # Update price for the corresponding latch block
                
                latch_data = HW_prices["Latch Plate"].get(selected_latch, None)

                block_data = HW_prices["Custom Latch Block"].get(paired_block, None)
                if block_data:
                    # st.write(f"HardwareID: {block_data['id']}")
                    total_price += block_data['price']
                    
                    if "Custom Latch Block" not in hwid:
                        hwid["Custom Latch Block"] = []

                    if block_data.get('id'):
                        hwid["Custom Latch Block"].append(block_data['id'])
    
  

st.divider()

# check flag
all_mandatory_filled = all(mandatory_flags.values())

if all_mandatory_filled:
    st.markdown(f"<p class='verdana-large'>Total Price: ${total_price:.3f}</p>", unsafe_allow_html=True)
    # st.write(f"### Total Price: ${total_price:.3f}")
else:
    st.markdown('<p class="verdana-large">Please complete all mandatory selections to see the total price.</p>', unsafe_allow_html=True)
    # st.write("### Please complete all mandatory selections to see the total price.")

if st.button("Generate IDs"):
    st.session_state['table'] = [['' for _ in columns] for _ in range(initial_rows)]
    update_table(0, 0, input_door)
    # st.write(hwid)
    for key, values in hwid.items():
        # Use the first value from the list (assuming there's only one per key)
        update_table_by_key(0, key, values[0])
    st.write("Part ID List Preview:")
    st.table([columns] + st.session_state['table'])


