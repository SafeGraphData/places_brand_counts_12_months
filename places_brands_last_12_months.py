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
# Keep-alive comment: 2025-05-07 22:23:26.609832
# Keep-alive comment: 2025-05-08 09:23:19.190617
# Keep-alive comment: 2025-05-08 20:23:26.925472
# Keep-alive comment: 2025-05-09 07:23:34.753601
# Keep-alive comment: 2025-05-09 18:23:47.801170
# Keep-alive comment: 2025-05-10 05:23:24.437308
# Keep-alive comment: 2025-05-10 16:23:18.602813
# Keep-alive comment: 2025-05-11 03:23:19.174197
# Keep-alive comment: 2025-05-11 14:23:10.740010
# Keep-alive comment: 2025-05-12 01:23:16.024018
# Keep-alive comment: 2025-05-12 12:23:46.052729
# Keep-alive comment: 2025-05-12 23:23:19.738109
# Keep-alive comment: 2025-05-13 10:24:19.029966
# Keep-alive comment: 2025-05-13 21:23:20.347428
# Keep-alive comment: 2025-05-14 08:23:46.175832
# Keep-alive comment: 2025-05-14 19:23:45.543746
# Keep-alive comment: 2025-05-15 06:23:46.861293
# Keep-alive comment: 2025-05-15 17:24:10.892421
# Keep-alive comment: 2025-05-16 04:23:32.117082
# Keep-alive comment: 2025-05-16 15:22:34.791273
# Keep-alive comment: 2025-05-17 02:22:53.299238
# Keep-alive comment: 2025-05-17 13:23:27.219356
# Keep-alive comment: 2025-05-18 00:22:51.712431
# Keep-alive comment: 2025-05-18 11:23:20.003538
# Keep-alive comment: 2025-05-18 22:23:17.432285
# Keep-alive comment: 2025-05-19 09:23:53.307998
# Keep-alive comment: 2025-05-19 20:22:52.380278
# Keep-alive comment: 2025-05-20 07:23:08.452463
# Keep-alive comment: 2025-05-20 18:24:20.550847
# Keep-alive comment: 2025-05-21 05:22:52.376514
# Keep-alive comment: 2025-05-21 16:23:01.305932
# Keep-alive comment: 2025-05-22 03:22:55.921368
# Keep-alive comment: 2025-05-22 14:22:59.499566
# Keep-alive comment: 2025-05-23 01:22:58.383148
# Keep-alive comment: 2025-05-23 12:22:58.204965
# Keep-alive comment: 2025-05-23 23:23:02.331375
# Keep-alive comment: 2025-05-24 10:23:00.131066
# Keep-alive comment: 2025-05-24 21:22:56.832292
# Keep-alive comment: 2025-05-25 08:22:57.516209
# Keep-alive comment: 2025-05-25 19:23:02.275389
# Keep-alive comment: 2025-05-26 06:22:47.525914
# Keep-alive comment: 2025-05-26 17:22:51.914046
# Keep-alive comment: 2025-05-27 04:22:57.467570
# Keep-alive comment: 2025-05-27 15:23:01.898241
# Keep-alive comment: 2025-05-28 02:23:11.523927
# Keep-alive comment: 2025-05-28 13:23:00.769131
# Keep-alive comment: 2025-05-29 00:22:55.389154
# Keep-alive comment: 2025-05-29 11:22:50.456546
# Keep-alive comment: 2025-05-29 22:23:04.943086
# Keep-alive comment: 2025-05-30 09:22:49.973906
# Keep-alive comment: 2025-05-30 20:22:50.927026
# Keep-alive comment: 2025-05-31 07:23:03.230994
# Keep-alive comment: 2025-05-31 18:22:57.800217