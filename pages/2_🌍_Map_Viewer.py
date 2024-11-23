import streamlit as st
import pydeck as pdk
from pydeck.types import String
from utils.data_loader import load_df
from enum import Enum
import pandas as pd
import os

MASTER_FILE="AUG_MASTER.txt"

class OwnershipType(Enum):
    INDIVIDUAL = 1
    PARTNERSHIP = 2
    CORPORATION = 3
    CO_OWNED = 4
    GOVERNMENT = 5
    LLC = 7
    NON_CITIZEN_CORPORATION = 8
    NON_CITIZEN_CO_OWNED = 9

    # Define a method to return the color for each type
    def color(self):
        return {
            OwnershipType.INDIVIDUAL: [255, 0, 0, 160],  # Red
            OwnershipType.PARTNERSHIP: [0, 255, 0, 160],  # Green
            OwnershipType.CORPORATION: [0, 0, 255, 160],  # Blue
            OwnershipType.CO_OWNED: [255, 255, 0, 160],  # Yellow
            OwnershipType.GOVERNMENT: [255, 165, 160],  # Orange
            OwnershipType.LLC: [128, 0, 128, 160],  # Purple
            OwnershipType.NON_CITIZEN_CORPORATION: [0, 255, 255, 160],  # Cyan
            OwnershipType.NON_CITIZEN_CO_OWNED: [128, 128, 128, 160],  # Gray
        }.get(self, [200, 200, 200, 160])  # Default gray for undefined types


class AircraftType(Enum):
    GLIDER = 1
    BALLOON = 2
    BLIMP_DIRIGIBLE = 3
    FIXED_WING_SINGLE_ENGINE = 4
    FIXED_WING_MULTI_ENGINE = 5
    ROTORCRAFT = 6
    WEIGHT_SHIFT_CONTROL = 7
    POWERED_PARACHUTE = 8
    GYROPLANE = 9
    HYBRID_LIFT = "H"
    OTHER = "O"

st.set_page_config(page_title="Map Viewer", page_icon="🌍")

st.markdown("# Map Viewer")
st.sidebar.header("Map Viewer")

master_df = load_df(MASTER_FILE, usecols=['TYPE REGISTRANT', 'TYPE AIRCRAFT', 'LONGITUDE', 'LATITUDE'])

# extract ownership
master_df['Ownership'] = pd.to_numeric(master_df['TYPE REGISTRANT'], errors='coerce')
master_df['OwnershipType'] = master_df['Ownership'].map(lambda x: OwnershipType(x).name if pd.notna(x) else 'UNKNOWN')
master_df['OwnershipColor'] = master_df['Ownership'].map(lambda x: OwnershipType(x).color() if pd.notna(x) else [200, 200, 200, 160])

# extract type aircraft
master_df['AircraftType'] = pd.to_numeric(master_df['TYPE AIRCRAFT'], errors='coerce')
master_df['AircraftType'] = master_df['AircraftType'].map(lambda x: AircraftType(x).name if pd.notna(x) else 'UNKNOWN')

hex_radius = st.sidebar.slider('Hexagon Radius', min_value=2000, max_value=100000, value=20000, step=1000)
scatter_radius = st.sidebar.slider('Scatter Radius', min_value=2000, max_value=500000, value=100000, step=1000)
ALL_LAYERS = {
    # "Hexagon": pdk.Layer(
    #     "HexagonLayer",
    #     data=master_df,
    #     get_position=["LONGITUDE", "LATITUDE"],
    #     radius=hex_radius,
    #     elevation_scale=4,
    #     elevation_range=[0, 1000],
    #     extruded=True,
    # ),
    "Scatter": pdk.Layer(
        "ScatterplotLayer",
        data=master_df,
        get_position=["LONGITUDE", "LATITUDE"],
        get_color="OwnershipColor",
        pickable=True,
        auto_highlight=True,
        get_radius=scatter_radius,
        radius_scale=0.05,
    ),
    "Heatmap":pdk.Layer(
        "HeatmapLayer",  # Layer type for heatmap
        data=master_df,  # DataFrame with lat/lon points
        get_position=["LONGITUDE", "LATITUDE"],
        get_weight=1,
        radius=scatter_radius,  # Radius of the area affected by each data point
        opacity=0.6,  # Opacity of the heatmap
        threshold=0.1  # Threshold for intensity (values between 0 and 1)
    )
}

st.sidebar.markdown("### Map Layers")
selected_layers = [
    layer
    for layer_name, layer in ALL_LAYERS.items()
    if st.sidebar.checkbox(layer_name, True)
]

theme = st.sidebar.radio(
    "Mapbox Style",
    ["light", "dark", "outdoors", "satellite"],
    horizontal=True
)
if theme == "dark":
    map_style="mapbox://styles/mapbox/dark-v11"
elif theme == "light":
    map_style="mapbox://styles/mapbox/light-v11"
elif theme == "outdoors":
    map_style="mapbox://styles/mapbox/outdoors-v12"
elif theme == "satellite":
    map_style="mapbox://styles/mapbox/satellite-streets-v12"
else:
    map_style="mapbox://styles/mapbox/light-v11"

if selected_layers:
    st.pydeck_chart(
        pdk.Deck(
            map_style=map_style,
            initial_view_state={
                "latitude": 36.52,
                "longitude": -95.02,
                "zoom": 3,
                "pitch": 20,
            },
            layers=selected_layers,
            tooltip={"text": "N-{N-NUMBER} {AircraftType}\n{YEAR MFR}, {OwnershipType}"}
        )
    )
else:
    st.error("Please choose at least one layer above.")