import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection
from google.oauth2 import service_account
from google.cloud import bigquery
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


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
def bq_query(query, output_type="dataframe"):
    query_job = client.query(query)
    if output_type == "dataframe":
        df = query_job.to_dataframe()
        return df
    
    if output_type == "rows":
        rows_raw = query_job.result()
        # Convert to list of dicts. Required for st.cache_data to hash the return value.
        rows = [dict(row) for row in rows_raw]
        return rows

def run_query(query, output_type="dataframe", use_cache=True):
    if use_cache:
        @st.cache_data(ttl=600)
        def run_cached_query(query, output_type="dataframe"):
            return bq_query(query, output_type=output_type)
        return run_cached_query(query, output_type=output_type)
    else:
        return bq_query(query, output_type=output_type)
        

@st.cache_data(ttl=600)
def list_tables():
    dataset_ref = client.dataset("parts", project="agentfocus")
    tables = client.list_tables(dataset_ref)
    table_ids = [table.table_id for table in tables]
    return table_ids[::-1]

def create_table(table_id, schema):
    """
    This function only creates the table when doest not exist
    """
    # Define dataset and table details
    project_id = "agentfocus"
    dataset_id = "general"
    # Full table reference
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Check if the table exists
    try:
        client.get_table(table_ref)  # Check if the table exists
        print(f"Table {table_ref} already exists.")
    except Exception:  # Table does not exist
        print(f"Table {table_ref} does not exist. Creating table...")
        # Create a table object
        table = bigquery.Table(table_ref, schema=schema)
        # Create the table in BigQuery
        table = client.create_table(table)
        print(f"Table {table_ref} created successfully.")

def insert_rows_json(table_id, rows_to_insert):
    project_id = "agentfocus"
    dataset_id = "general"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))