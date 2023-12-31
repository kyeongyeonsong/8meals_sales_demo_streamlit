import streamlit as st
#import plotly.express as px
from collections import defaultdict
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

st.set_page_config(
    page_title="8Meals",
    page_icon="👋",
)

st.write("# 8Meals Sales 👋")

st.sidebar.success("Select a demo above.")

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

def convert_to_dict(row):
    return {
        '매장': row.매장,
        '대분류': row.대분류,
        '중분류': row.중분류,
        '소분류': row.소분류,
        '상품코드': row.상품코드,
        '상품명': row.상품명,
        '매출': row.매출
    }

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=60)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    print(rows[0])
    return [convert_to_dict(row) for row in rows]

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
#st.write(rows[0])

# Step 1: Aggregate data by '대분류' and sum '판매가'
total_sales_by_category = defaultdict(int)

for row in rows:
    category = row['대분류']
    price = row['매출']
    if price is not None:
        total_sales_by_category[category] += price

# Step 3: Draw Line Chart
st.line_chart(total_sales_by_category)

# Aggregate data by '중분류' and sum '판매가'
total_sales_by_subcategory = defaultdict(int)

for row in rows:
    subcategory = row['중분류']
    price = row['매출']
    if price is not None:
         total_sales_by_subcategory[subcategory] += price

st.line_chart(total_sales_by_subcategory)

total_sales_by_smallcategory = defaultdict(int)

for row in rows:
    smallcategory = row['소분류']
    price = row['매출']
    if price is not None:
         total_sales_by_smallcategory[smallcategory] += price

st.line_chart(total_sales_by_smallcategory)
