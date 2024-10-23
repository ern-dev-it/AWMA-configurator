import pandas as pd

df = pd.read_csv('SQL_Base.csv')
df1 = pd.read_csv('SQL_HardWare.csv')

def convert_currency(value):
    return float(value.replace('$', '').replace(',', ''))

def cleanBasePriceData(df):
    df.columns = df.columns.str.strip()
    df = df.loc[:,["DoorSizeID", "Size",
                  "UnitSellToAWMA","ThicknessType"]]
    return df

def cleanHWPriceData(df):
    df.columns = df.columns.str.strip()
    df = df.loc[:,["HardwareID","ApplicableDoorType", "HardwareType",
                  "Description","UnitSell"]]
    
    rename_mapping = {
        "Mortice Locks": "Mortice",
        "Latch": "Latch Plate",
        "Machine Block": "Custom Latch Block",
        "Exterior handles": "Exterior Plate/Handle (Optional)",
        "Interior handles": "Interior Plate/Handle",
        "Additional Hardware": "Additional Hardware (Optional)"
    }
    
    # Apply the mapping to the 'Hardware Type' column
    df['HardwareType'] = df['HardwareType'].replace(rename_mapping)
    return df

def getBasePrice(df):
    df = cleanBasePriceData(df)

    base_price_dict = {}
    for index, row in df.iterrows():
        size = row['Size']
        door_type = row['ThicknessType']
        price = row['UnitSellToAWMA']
        item_id = row['DoorSizeID']
        
        if size not in base_price_dict:
            base_price_dict[size] = {}

        base_price_dict[size][door_type] = {
            'price': price,
            'id': item_id
        }
    
    return base_price_dict

def getHWPrice(df, door_type):
    df = cleanHWPriceData(df)

    if door_type == "Standard": # if standard
        df_filtered = df.drop(df[df["ApplicableDoorType"] == "Fully Sealed"].index)
    else: # if fully sealed
        df_filtered = df.drop(df[df["ApplicableDoorType"] == "Standard"].index)

    HW_prices_dict = {}
    
    for index, row in df_filtered.iterrows():
        hardware_type = row['HardwareType']
        description = row['Description']
        price = row['UnitSell']
        item_id = row['HardwareID']

        if hardware_type not in HW_prices_dict:
            HW_prices_dict[hardware_type] = {}
        
        HW_prices_dict[hardware_type][description] = {
            'price': price,
            'id': item_id
        }

        for hardwareType in HW_prices_dict:
            HW_prices_dict[hardwareType] = {"Select an option...": None, **HW_prices_dict[hardwareType]}
    
    return HW_prices_dict


'''
test = getBasePrice(df)
print("Here's the output of getBasePrice")
print(test)

test2 = getHWPrice(df1, 1)
print("Here's the output of getHWPrice")
print(test2)
'''