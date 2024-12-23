import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_df
import os

st.set_page_config(
    page_title="Aviator Toolbox",
    page_icon="👋",
)

st.markdown("# Welcome to Aviator Toolbox! 👋")
st.markdown(
    """
    Here is a collection of tools for aviators.
    
    Data [source](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download)

    Github [source](https://github.com/ss-zheng/faa-view)
    """
)
st.sidebar.success("Select a viewer above.")
