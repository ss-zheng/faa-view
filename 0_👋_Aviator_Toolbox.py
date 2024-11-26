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

import streamlit.components.v1 as components
base_url = "https://www.stockmarket.aero/"
iframe_src = base_url
components.iframe(iframe_src, height=500, scrolling=True)


with open("/tmp/table.html", "r") as file:
    html_content = file.read()

from bs4 import BeautifulSoup
from urllib.parse import urljoin

# # Find and remove all <img> tags
# for img in soup.find_all("img"):
#     img.decompose()  # Remove the <img> tag from the document


# Base URL to prepend
base_url = "https://www.stockmarket.aero/"

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find all <a> tags and update relative hrefs
for a_tag in soup.find_all("a", href=True):
    # Convert relative URLs to absolute using urljoin
    a_tag['href'] = urljoin(base_url, a_tag['href'])

for img_tag in soup.find_all("img", src=True):
    # Convert relative URLs to absolute using urljoin
    img_tag['src'] = urljoin(base_url, img_tag['src'])

# Print the modified HTML
cleaned_html = soup.prettify()
st.write(cleaned_html)
st.html(cleaned_html)