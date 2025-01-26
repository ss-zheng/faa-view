import streamlit as st
from components.header import header

st.set_page_config(
    page_title="Aviator Toolbox",
    page_icon="👋",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
header()

st.sidebar.success("Select a viewer above.")

st.markdown("# Welcome to Aviator Toolbox! 👋")
st.markdown(
    """
    Here is a collection of tools for aviators.
    
    Data [source](https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download)

    Github [source](https://github.com/ss-zheng/faa-view)
    """
)