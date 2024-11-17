import os
# from ..utils.data_loader import load_df
import pandas as pd
from geopy.exc import GeopyError, GeocoderUnavailable
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
tqdm.pandas()
pd.options.display.width = 0
pd.options.display.max_colwidth = 100
pd.options.display.max_columns = None
pd.options.display.max_rows = None

def load_df(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError as e:
        raise e


DB_FOLDER="./data/ReleasableAircraft"
MASTER_FILE=os.path.join(DB_FOLDER, "MASTER.txt")
AUG_MASTER_FILE=os.path.join(DB_FOLDER, "AUG_MASTER.txt")

master_df = load_df(MASTER_FILE)
# master_df = master_df.head(1000)

geolocator = Nominatim(user_agent="faa-viewer")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.01, max_retries=2)

def geocode_location(row):
    full_address = row['FULL_ADDRESS']
    partial_address = row['PARTIAL_ADDRESS']
    location = None  # Default value in case both geocoding attempts fail
    try:
        # Try geocoding with full address first
        location = geocode(full_address)
        if location is None:  # Explicitly check if the full address was not found
            print(f"Full address not found: {full_address}")
            # Fallback to partial address if full address fails
            location = geocode(partial_address)
        
    except GeopyError as e:
        print(f"Geocoding error for full address: {full_address} - {e}")
        # Attempt with partial address after full address fails
        try:
            location = geocode(partial_address)
        except GeopyError as e:
            print(f"Geocoding error for partial address: {partial_address} - {e}")
            print(f"Skipping row: {row}")
    return location

#TODO: try us the full_address and fall back to city when cannot find
master_df['FULL_ADDRESS'] = master_df.apply(lambda row: f"{row['STREET'].strip()}, {row['CITY'].strip()}, {row['STATE']}, {row['COUNTRY']}", axis=1)
master_df['PARTIAL_ADDRESS'] = master_df.apply(lambda row: f"{row['CITY'].strip()}, {row['STATE']}, {row['COUNTRY']}", axis=1)

# get geolocation base on FULL ADDRESS first, if failed then try PARTIAL ADDRESS
master_df['LOCATION'] = master_df[['FULL_ADDRESS', 'PARTIAL_ADDRESS']].progress_apply(geocode_location, axis=1)
master_df['POINT'] = master_df['LOCATION'].apply(lambda loc: tuple(loc.point) if loc else None)
# given master_df LOCATION col, extra two column lat lon
master_df['LATITUDE'] = master_df['LOCATION'].apply(lambda loc: loc.latitude if loc else None)
master_df['LONGITUDE'] = master_df['LOCATION'].apply(lambda loc: loc.longitude if loc else None)


print(master_df[['N-NUMBER', 'CITY', 'LOCATION', 'POINT']].head())
master_df.to_csv(AUG_MASTER_FILE)


