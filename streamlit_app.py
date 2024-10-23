import pandas as pd
import streamlit as st

from data_processing import getBasePrice, getHWPrice

df = pd.read_csv('SQL_Base.csv')
df1 = pd.read_csv('SQL_HardWare.csv')

st.title("AWMA configurator")

st.write("Step 1: Select type of door and size")
col1, col2 = st.columns(2)

door_prices = getBasePrice(df)
with col1:
    door_type = st.radio("Select Door Type:", ["Standard", "Fully Sealed"], horizontal = True)  
with col2:
    door_size = st.selectbox("Select Door Size:", list(door_prices.keys()))

doorprice = door_prices[door_size][door_type]

# st.write(f"Selected Door Type: {door_type}")
# st.write(f"Selected Door Size: {door_size}")
#st.write("Base Price:" + doorprice)

st.divider()

st.write("Step 2: Select Hinge Type")
hinge_type = st.radio("", ["Left hinge", "Right hinge"], horizontal = True)

st.divider()

st.write("Step 3: Select hardware required")

# gonna get ugly please don't puke when you read these:

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

### need review!!
if door_type in door_prices[door_size]:
    # Retrieve filtered dataset based on door type
    HW_prices = getHWPrice(df1, door_type)
    # total_price = float(doorprice.replace('$', '').replace(',', '').strip())
    total_price = doorprice

    # Put categories into orders, matching the order in macros
    ordered_categories = [
    "Mortice",
    "Latch Plate",
    "Exterior Plate/Handle (Optional)",
    "Interior Plate/Handle",
    "Additional Hardware (Optional)"
    ]

    selected_latch = None

    for category in ordered_categories:
        if category not in HW_prices:
            continue

        # create selection box for each category
        selected_item = st.selectbox(f"Select {category}:", list(HW_prices[category].keys()))

        if category == "Latch Plate":
            selected_latch = selected_item

            if selected_latch in latch_to_latch_block[door_type]:
                # Get the paired latch block based on the door type
                paired_block = latch_to_latch_block[door_type][selected_latch]
                
                # Create a selection box but only show the paired block as the sole option
                st.selectbox("Paired Latch Block:", [paired_block])
                
                # Update price for the corresponding latch block
                if paired_block != "None Required" and paired_block in HW_prices["Custom Latch Block"]:
                    price = HW_prices["Custom Latch Block"][paired_block]
                    total_price += price
                    # st.write(f"Price for {paired_block}: ${price:.2f}")

        # update mandatory field flag
        if category in mandatory_categories:
            mandatory_flags[category] = selected_item != "Select an option..."
        # append price
        if selected_item != "Select an option..." and HW_prices[category][selected_item] is not None:
            # price_str = HW_prices[category][selected_item].strip().replace('$', '').replace(',', '')
            price = HW_prices[category][selected_item]
            total_price += price
            #st.write(f"Price for {selected_item}: ${price:.2f}")
    
    

st.divider()
# check flag
all_mandatory_filled = all(mandatory_flags.values())

# total_price = float(total_price)
# only print total price if all mandatory fields are filled
if all_mandatory_filled:
    st.write(f"### Total Price: ${total_price:.2f}")
else:
    st.write("### Please complete all mandatory selections to see the total price.")

holder = ["Mortice:","Latch Plate:","Custom Latch Block:", "Exterior Plate/ Handle:", "Interior Plate/ Handle:", "Additional Hardware:"]

