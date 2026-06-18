import pandas as pd
import numpy as np
import zipcodes
from sklearn.preprocessing import LabelEncoder
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.distance import haversine
from utils.factory_config import FACTORIES, PRODUCT_FACTORY_MAP
def get_lat_lon(zip_code):
    try:
        match = zipcodes.matching(str(zip_code))
        if match:
            return float(match[0]['lat']), float(match[0]['long'])
    except:
        pass
    return 0.0, 0.0
def prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days
    df = df[df['Lead Time'] > 0]
    df['Current Factory'] = df['Product Name'].map(PRODUCT_FACTORY_MAP)
    coords = df['Postal Code'].apply(get_lat_lon)
    df['Cust_Lat'] = [c[0] for c in coords]
    df['Cust_Lon'] = [c[1] for c in coords]
    for f_name, f_coords in FACTORIES.items():
        safe_name = f_name.replace(" ", "_").replace("'", "")
        df["Dist_" + safe_name] = df.apply(lambda row: haversine(row['Cust_Lat'], row['Cust_Lon'], f_coords['lat'], f_coords['lon']), axis=1)
    df['Ship_Mode_Enc'] = LabelEncoder().fit_transform(df['Ship Mode'].astype(str))
    df['Region_Enc'] = LabelEncoder().fit_transform(df['Region'].astype(str))
    df['Product_Enc'] = LabelEncoder().fit_transform(df['Product Name'].astype(str))
    return df
