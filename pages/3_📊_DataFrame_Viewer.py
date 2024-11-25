import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from utils.data_loader import load_df
import os

st.set_page_config(
    page_title="Dataframe Viewer",
    page_icon="📊",
    layout="wide"
    )

st.markdown("# Dataframe Viewer")
st.sidebar.header("Dataframe Viewer")

MASTER_FILE="MASTER.txt"
ACFTREF_FILE="ACFTREF.txt"
DEALER_FILE="DEALER.txt"
top_n = st.sidebar.slider("Top n aircraft models", min_value=10, max_value=100, value=10)
n_rows = st.sidebar.slider("Show n rows", min_value=10, max_value=1000, value=10)

def display_df(df):
    st.write(df.shape)
    st.dataframe(df.head(n_rows))

master_df = load_df(MASTER_FILE)
acftref_df = load_df(ACFTREF_FILE)
dealer_df = load_df(DEALER_FILE)

stat_df = master_df.groupby("MFR MDL CODE").size().reset_index(name="count")
# Sort the DataFrame by 'count' in descending order
stat_df = stat_df.sort_values(by="count", ascending=False).reset_index(drop=True).head(top_n)
merged_df = pd.merge(stat_df, acftref_df[["CODE", "MFR", "MODEL"]], left_on="MFR MDL CODE", right_on="CODE", how="left")
merged_df["MFR_MODEL"] = merged_df.apply(lambda row: row["MFR"].strip() + " " +row["MODEL"].strip(), axis=1)
# st.dataframe(merged_df)

chart = alt.Chart(merged_df).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x='count:Q',
        y=alt.Y('MFR_MODEL:N', sort=alt.EncodingSortField(field='count', op='sum', order='descending'), axis=alt.Axis(labelAngle=0, labelLimit=200)),
    )

st.markdown("## Top N Aircraft Models")
st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.markdown("## Preview MASTER file:")
display_df(master_df)

st.markdown("## Preview ACFTREF file:")
display_df(acftref_df)

st.markdown("## Preview DEALER file:")
display_df(dealer_df)