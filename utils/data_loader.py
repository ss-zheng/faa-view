import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection
import os

def load_df(filename, usecols=None):
    try:
        if os.path.isdir("data"):
            file_path = os.path.join("data/ReleasableAircraft", filename)
            df = pd.read_csv(file_path, usecols=usecols)
        else:
            # Create connection object and retrieve file contents.
            # Specify input format is a csv and to cache the result for 600 seconds.
            conn = st.connection('gcs', type=FilesConnection)
            file_path = os.path.join("faa-viewer-bucket/ReleasableAircraft", filename)
            df = conn.read(file_path, input_format="csv", usecols=usecols, ttl=600) # ttl controls cache time
        return df
    except FileNotFoundError as e:
        raise e