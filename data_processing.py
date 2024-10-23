import pandas as pd

df = pd.read_csv('SQL_Base.csv')
df1 = pd.read_csv('SQL_HardWare.csv')

def convert_currency(value):
    return float(value.replace('$', '').replace(',', ''))

def cleanBasePriceData(df):
    df.columns = df.columns.str.strip()
    df = df.loc[:,["DoorSizeID", "Size",
                  "UnitSellToAWMA","ThicknessType"]]
    #df['amount'] = df['UnitSellToAWMA'].apply(convert_currency)
    return df

def cleanHWPriceData(df):
    df.columns = df.columns.str.strip()
    df = df.loc[:,["HardwareID","ApplicableDoorType", "HardwareType",
                  "Description","UnitSell"]]
    #df['amount'] = df['Unit Sell'].apply(convert_currency)
    
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
    door_prices = {}
    for index, row in df.iterrows():
        size = row['Size']
        price = row['UnitSellToAWMA']
        door_type = row['ThicknessType']
        
        if size not in door_prices:
            door_prices[size] = {}  # Initialize nested dictionary
        
        door_prices[size][door_type] = price

    return door_prices

def getHWPrice(df, type):
    df = cleanHWPriceData(df)
    if type == "Standard": # if standard
        df_filtered = df.drop(df[df["ApplicableDoorType"] == "Fully Sealed"].index)
    else: # if fully sealed
        df_filtered = df.drop(df[df["ApplicableDoorType"] == "Standard"].index)

    HW_prices = {}
    for index, row in df_filtered.iterrows():
        hardwareType = row['HardwareType']
        price = row['UnitSell']
        desc = row['Description']
        
        if hardwareType not in HW_prices:
            HW_prices[hardwareType] = {}

        HW_prices[hardwareType][desc] = price
        
        for hardwareType in HW_prices:
            HW_prices[hardwareType] = {"Select an option...": None, **HW_prices[hardwareType]}
    
    return HW_prices

'''
test = getBasePrice(df)
print("Here's the output of getBasePrice")
print(test)

test2 = getHWPrice(df1, 1)
print("Here's the output of getHWPrice")
print(test2)
'''