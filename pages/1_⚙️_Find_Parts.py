import streamlit as st
import streamlit.components.v1 as components
from utils.aviation_se import google_search, display_response
from utils.data_loader import run_query, list_tables
from components.header import header

st.set_page_config(
    page_title="Parts Finder",
    page_icon="⚙️",
    layout="wide"
)
header()

st.markdown("# Find Parts ⚙️")

st.sidebar.markdown("[New Parts Today](#new-parts-today)")
ui_tables = list_tables()
new_table = st.sidebar.selectbox(
    "new_table",
    ui_tables,
    index=0,
)
old_table = st.sidebar.selectbox(
    "old_table",
    ui_tables,
    index=1,
)

st.sidebar.markdown("[Search Parts](#search-parts)")
st.sidebar.markdown("[Third-Party Search](#third-party-search)")

query_template = """
SELECT 
  CASE 
    WHEN ARRAY_LENGTH(new_table.imgs) > 0 THEN new_table.imgs[offset(0)] 
    ELSE NULL 
  END AS preview_img, 
  new_table.link,
  new_table.inventory_id,
  new_table.seller,
  new_table.category,
  new_table.subcategory,
  new_table.part_number,
  new_table.brand,
  new_table.title,
  new_table.price
FROM 
  `agentfocus.parts.{new_table}` AS new_table
LEFT JOIN 
  `agentfocus.parts.{old_table}` AS old_table
ON 
  new_table.inventory_id = old_table.inventory_id
WHERE 
  old_table.inventory_id IS NULL;
"""

def st_ui_df(df, expander_title=None, key=None, meta=None):
    if df.empty:
        st.write("No results found")
        return
    unique_sellers = df['seller'].unique()
    seller_selection = st.pills("Seller", unique_sellers, key=key, default=unique_sellers, selection_mode="multi")
    filtered_df = df[df['seller'].isin(seller_selection)]
    st.dataframe(
        filtered_df,
        column_order=[
            "preview_img",
            "link",
            "title",
            "part_number",
            "price",
            "category",
            "subcategory",
            "brand",
            "seller",
        ],
        hide_index=True,
        column_config={
        "preview_img": st.column_config.ImageColumn(help="Preview image"),
        "link": st.column_config.LinkColumn(display_text="🔗"),
        "title": st.column_config.Column(width="large"),
        "price": st.column_config.NumberColumn(format="$%d"),
    })
    stat_df = filtered_df.groupby(["category", "subcategory"]).size().reset_index(name="count")
    n_results = filtered_df.shape[0]
    with st.expander(f"{n_results} results | {expander_title}"):
        left, right = st.columns(2)
        left.write(filtered_df.shape[0])
        if meta:
            left.code(meta)
        right.dataframe(stat_df)

def compare_tables(new_table, old_table):
    st.markdown("## New Parts Today")
    query = query_template.format(new_table=new_table, old_table=old_table)
    df = run_query(query, output_type="dataframe")
    new_date = new_table.split("_")[1]
    old_date = old_table.split("_")[1]
    st_ui_df(df, expander_title=f"Compare {new_date} vs {old_date}", key="new_parts_pills", meta=query)

if st.sidebar.button("Compare"):
    compare_tables(new_table, old_table)
else:
    latest_table = ui_tables[0]
    second_latest_table = ui_tables[1]
    compare_tables(latest_table, second_latest_table)


st.markdown('## Search Parts')

search_input = st.text_input(
        "Search Term / Part Number",
        placeholder="KX155A / 069-01032-0101",
        on_change=lambda: setattr(st.session_state, 'search_page', 1)
        )

# search within our Universal Inventory
query_template = """
SELECT 
  CASE 
    WHEN ARRAY_LENGTH(imgs) > 0 THEN imgs[offset(0)] 
    ELSE NULL 
  END AS preview_img, 
  link,
  inventory_id,
  seller,
  category,
  subcategory,
  part_number,
  brand,
  title,
  price
FROM 
  `agentfocus.parts.{table_id}`
WHERE LOWER(title) LIKE '%{search_input}%' 
OR LOWER('{search_input}') IN UNNEST(ARRAY(SELECT LOWER(part_number) FROM UNNEST(part_number) AS part_number))
"""
if search_input:
    tab1, tab2, tab3 = st.tabs(["Inventory", "Google", "Ebay"])

    with tab1:
        query = query_template.format(table_id=new_table, search_input=search_input)
        # st.write(query)
        ui_df = run_query(query, output_type="dataframe")
        st_ui_df(ui_df, expander_title="Stats", key="search_ui_pills", meta=query)
    
    with tab2:
        if "search_page" not in st.session_state:
            st.session_state.search_page = 1

        # if 'response' not in st.session_state:
        #     st.session_state.response = {}
        # response = search(search_input)
        response = google_search(search_input, page=st.session_state.search_page)
        display_response(response)
    
    with tab3:
        # ebay quick search, this link jump directly to the right ebay category
        ebay_aviation_url = f"https://www.ebay.com/sch/26435/i.html?_from=R40&_nkw={search_input}"
        st.link_button("Jump to Ebay", ebay_aviation_url)


st.markdown("## Third-Party Search")
base_url = "https://www.stockmarket.aero/"
iframe_src = base_url
components.iframe(iframe_src, height=500, scrolling=True)