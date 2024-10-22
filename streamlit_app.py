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
    "Custom Latch Block",
    "Exterior Plate/Handle (Optional)",
    "Interior Plate/Handle",
    "Additional Hardware (Optional)"
    ]

    show_custom_latch_block = True

    for category in ordered_categories:
        if category not in HW_prices:
            continue
        # based on 'Latch Plate', skip displaying CLB when 'standard erntec latch' is selected
        if category == "Custom Latch Block" and not show_custom_latch_block:
            continue
        # create selection box for each category
        selected_item = st.selectbox(f"Select {category}:", list(HW_prices[category].keys()))
        # turn off the CLB flag based on the condition
        if category == "Latch Plate" and selected_item == "Standard Erntec Latch":
            show_custom_latch_block = False
        # update mandatory field flag
        if category in mandatory_categories:
            mandatory_flags[category] = selected_item != "Select an option..."
        # append price
        if selected_item != "Select an option..." and HW_prices[category][selected_item] is not None:
            # price_str = HW_prices[category][selected_item].strip().replace('$', '').replace(',', '')
            price_str = HW_prices[category][selected_item]
            price = float(price_str)
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

