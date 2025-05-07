import streamlit as st
from read_data import read_from_gsheets
import altair as alt
from datetime import datetime, timedelta
import pandas as pd
import streamlit.components.v1 as components
from math import floor, ceil



st.set_page_config(
    page_title="Places Summary Statistics - Brands Last 12 Months",
    layout="wide"
)
#### Brands By Country Last 12 months ####
global_places_df = (read_from_gsheets("Global Places").query('Country  != "Excluding US"').reset_index(drop=True))
global_places_df = global_places_df[["Release month", "Country", "Distinct brands"]]

for i, value in enumerate(global_places_df['Release month']):
    try:
        global_places_df.loc[i, 'Release month'] = pd.to_datetime(value, format='%b %Y').strftime('%Y-%m')
    except ValueError:
        global_places_df.loc[i, 'Release month'] = pd.to_datetime(value, format='%B %Y').strftime('%Y-%m')

start_date_str = (datetime.now() - timedelta(days=365)).strftime("%Y-%m")

global_places_df["Release month"] = pd.to_datetime(global_places_df["Release month"])
brands_by_country_df = global_places_df[
    (global_places_df["Release month"] >= start_date_str) & (global_places_df["Release month"] <= datetime.now()) &
    (global_places_df["Country"] != "Grand Total")
]
brands_by_country_df["Release month"] = pd.to_datetime(brands_by_country_df["Release month"])+ pd.DateOffset(1)
brands_by_country_df["Release month"] = brands_by_country_df["Release month"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
brands_by_country_df["Distinct brands"] = pd.to_numeric(brands_by_country_df["Distinct brands"])

# st.dataframe(brands_by_country_df)

brands_by_country = alt.Chart(brands_by_country_df).mark_bar().encode(
    x=alt.X('Release month', timeUnit='yearmonth'),
    y='Distinct brands',
    color=alt.Color('Country', scale=alt.Scale(scheme='redyellowblue')),
    tooltip=[alt.Tooltip('Release month', timeUnit='yearmonth', title='Release month'),
             alt.Tooltip('Country'),
             alt.Tooltip('Distinct brands', format=',')]
).properties(
    width=900,
    height=500,
    title=alt.TitleParams(
        text='Distinct Brand Count by Country - Last 12 months',
        fontSize=18
    )
).configure_axisY(
    labelAngle=0
).configure_axisX(
    title=None,
    labelAngle=45
)

st.altair_chart(brands_by_country, use_container_width=True)

#### Overall Brands Last 12 Months ####
global_places_df = (read_from_gsheets("Global Places").query('Country  != "Excluding US"').reset_index(drop=True))
global_places_df = global_places_df[["Release month", "Country", "Distinct brands"]]

for i, value in enumerate(global_places_df['Release month']):
    try:
        global_places_df.loc[i, 'Release month'] = pd.to_datetime(value, format='%b %Y').strftime('%Y-%m')
    except ValueError:
        global_places_df.loc[i, 'Release month'] = pd.to_datetime(value, format='%B %Y').strftime('%Y-%m')

start_date_str = (datetime.now() - timedelta(days=365)).strftime("%Y-%m")

global_places_df["Release month"] = pd.to_datetime(global_places_df["Release month"])
overall_brands_last_12_df = global_places_df[
    (global_places_df["Release month"] >= start_date_str) & (global_places_df["Release month"] <= datetime.now()) &
    (global_places_df["Country"] == "Grand Total")
]
overall_brands_last_12_df["Release month"] = pd.to_datetime(overall_brands_last_12_df["Release month"])+ pd.DateOffset(1)
overall_brands_last_12_df["Release month"] = overall_brands_last_12_df["Release month"].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
overall_brands_last_12_df["Distinct brands"] = pd.to_numeric(overall_brands_last_12_df["Distinct brands"])
overall_brands_last_12_df = overall_brands_last_12_df.rename(columns={"Distinct brands": "Distinct brands - overall"})

# st.dataframe(overall_brands_last_12_df)


y_min = overall_brands_last_12_df['Distinct brands - overall'].min()
y_max = overall_brands_last_12_df['Distinct brands - overall'].max()
y_min_rounded = floor(y_min / 1000) * 1000
y_max_rounded =ceil(y_max / 1000) * 1000
y_range = [ y_min_rounded,y_max_rounded ]
y_ticks = list(range(y_min_rounded, y_max_rounded, 1000)) 

st.markdown('##### &nbsp;&nbsp;&nbsp;Distinct Brand Count Overall - Last 12 months')
overall_brands_last_12 = alt.Chart(overall_brands_last_12_df).mark_line().encode(
    x=alt.X('Release month', timeUnit='yearmonth'),
    y=alt.Y('Distinct brands - overall', scale=alt.Scale(domain=y_range)),
    tooltip=[alt.Tooltip('Release month', timeUnit='yearmonth', title='Release month'),
             alt.Tooltip('Country'),
             alt.Tooltip('Distinct brands - overall', format=',')]
)

boxes = alt.Chart(overall_brands_last_12_df).mark_line(strokeWidth=100, opacity=0.01).encode(
    x=alt.X('Release month', timeUnit='yearmonth'),
    y=alt.Y('Distinct brands - overall', scale=alt.Scale(domain=y_range)),
    tooltip=[alt.Tooltip('Release month', timeUnit='yearmonth', title='Release month'),
             alt.Tooltip('Country'),
             alt.Tooltip('Distinct brands - overall', format=',')]
)

combined = (
    overall_brands_last_12 + boxes
).properties(
    width=800,
    height=400,
    title=alt.TitleParams(
        text='',#'Distinct Brand Count Overall - Last 12 months',
        fontSize=18
    )
).configure_axisX(
    title=None,
    labelAngle=45
).configure_axisY(
    tickCount=len(y_ticks),
    values=y_ticks
)

st.altair_chart(combined,use_container_width=True)


hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

css = '''
<style>
section.main > div:has(~ footer ) {
     padding-top: 0px;
    padding-bottom: 0px;
}

[data-testid="ScrollToBottomContainer"] {
    overflow: hidden;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)


# Keep-alive comment: 2025-04-25 16:18:26.376051
# Keep-alive comment: 2025-04-26 00:24:01.156041
# Keep-alive comment: 2025-04-26 11:23:55.875732
# Keep-alive comment: 2025-04-26 22:22:55.190182
# Keep-alive comment: 2025-04-27 09:23:26.102631
# Keep-alive comment: 2025-04-27 20:23:20.981368
# Keep-alive comment: 2025-04-28 07:23:51.119601
# Keep-alive comment: 2025-04-28 18:24:11.361685
# Keep-alive comment: 2025-04-29 05:23:40.953795
# Keep-alive comment: 2025-04-29 16:24:25.367279
# Keep-alive comment: 2025-04-30 03:23:15.690308
# Keep-alive comment: 2025-04-30 14:23:43.610043
# Keep-alive comment: 2025-05-01 01:23:55.204225
# Keep-alive comment: 2025-05-01 12:23:26.345072
# Keep-alive comment: 2025-05-01 23:22:59.058914
# Keep-alive comment: 2025-05-02 10:23:45.146749
# Keep-alive comment: 2025-05-02 21:22:56.840202
# Keep-alive comment: 2025-05-03 08:23:21.273646
# Keep-alive comment: 2025-05-03 19:23:39.290980
# Keep-alive comment: 2025-05-04 06:23:44.884657
# Keep-alive comment: 2025-05-04 17:22:54.160490
# Keep-alive comment: 2025-05-05 04:24:04.608422
# Keep-alive comment: 2025-05-05 15:23:22.843680
# Keep-alive comment: 2025-05-06 02:24:15.147158
# Keep-alive comment: 2025-05-06 13:23:16.385803
# Keep-alive comment: 2025-05-07 00:23:15.666937
# Keep-alive comment: 2025-05-07 11:23:16.263312