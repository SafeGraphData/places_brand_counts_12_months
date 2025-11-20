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
# Keep-alive comment: 2025-06-01 05:22:55.980825
# Keep-alive comment: 2025-06-01 16:23:09.663760
# Keep-alive comment: 2025-06-02 03:23:11.328427
# Keep-alive comment: 2025-06-02 14:23:02.035930
# Keep-alive comment: 2025-06-03 01:22:52.461689
# Keep-alive comment: 2025-06-03 12:23:06.713304
# Keep-alive comment: 2025-06-03 23:23:02.281787
# Keep-alive comment: 2025-06-04 10:23:02.111867
# Keep-alive comment: 2025-06-04 21:22:40.498154
# Keep-alive comment: 2025-06-05 08:23:04.582313
# Keep-alive comment: 2025-06-05 19:22:54.066423
# Keep-alive comment: 2025-06-06 06:22:52.184619
# Keep-alive comment: 2025-06-06 17:22:35.497306
# Keep-alive comment: 2025-06-07 04:22:37.268854
# Keep-alive comment: 2025-06-07 15:22:46.441771
# Keep-alive comment: 2025-06-08 02:22:51.818581
# Keep-alive comment: 2025-06-08 13:22:53.719906
# Keep-alive comment: 2025-06-09 00:22:35.888449
# Keep-alive comment: 2025-06-09 11:22:50.359535
# Keep-alive comment: 2025-06-09 22:22:58.964285
# Keep-alive comment: 2025-06-10 09:23:02.035332
# Keep-alive comment: 2025-06-10 20:22:55.151471
# Keep-alive comment: 2025-06-11 07:22:56.201792
# Keep-alive comment: 2025-06-11 18:24:44.014879
# Keep-alive comment: 2025-06-12 05:22:53.387794
# Keep-alive comment: 2025-06-12 16:22:56.734801
# Keep-alive comment: 2025-06-13 03:22:57.803282
# Keep-alive comment: 2025-06-13 14:22:47.008566
# Keep-alive comment: 2025-06-14 01:23:06.863783
# Keep-alive comment: 2025-06-14 12:22:54.107241
# Keep-alive comment: 2025-06-14 23:22:45.527383
# Keep-alive comment: 2025-06-15 10:22:31.138054
# Keep-alive comment: 2025-06-15 21:23:05.840900
# Keep-alive comment: 2025-06-16 08:23:02.755042
# Keep-alive comment: 2025-06-16 19:22:46.768070
# Keep-alive comment: 2025-06-17 06:23:23.627781
# Keep-alive comment: 2025-06-17 17:22:51.636602
# Keep-alive comment: 2025-06-18 04:22:57.813737
# Keep-alive comment: 2025-06-18 15:22:56.414307
# Keep-alive comment: 2025-06-19 02:22:55.318905
# Keep-alive comment: 2025-06-19 13:22:54.959502
# Keep-alive comment: 2025-06-20 00:22:52.007620
# Keep-alive comment: 2025-06-20 11:23:41.164594
# Keep-alive comment: 2025-06-20 22:23:00.610358
# Keep-alive comment: 2025-06-21 09:22:46.167278
# Keep-alive comment: 2025-06-21 20:22:58.364045
# Keep-alive comment: 2025-06-22 07:22:51.208127
# Keep-alive comment: 2025-06-22 18:22:41.710460
# Keep-alive comment: 2025-06-23 05:22:58.182893
# Keep-alive comment: 2025-06-23 16:22:51.447246
# Keep-alive comment: 2025-06-24 03:22:57.869236
# Keep-alive comment: 2025-06-24 14:22:37.350657
# Keep-alive comment: 2025-06-25 01:22:31.640413
# Keep-alive comment: 2025-06-25 12:22:53.317785
# Keep-alive comment: 2025-06-25 23:22:55.896699
# Keep-alive comment: 2025-06-26 10:23:03.490937
# Keep-alive comment: 2025-06-26 21:24:27.854190
# Keep-alive comment: 2025-06-27 08:22:56.783244
# Keep-alive comment: 2025-06-27 19:22:53.387281
# Keep-alive comment: 2025-06-28 06:23:00.420802
# Keep-alive comment: 2025-06-28 17:22:50.705557
# Keep-alive comment: 2025-06-29 04:22:39.858894
# Keep-alive comment: 2025-06-29 15:22:30.430547
# Keep-alive comment: 2025-06-30 02:22:51.796667
# Keep-alive comment: 2025-06-30 13:22:33.238854
# Keep-alive comment: 2025-07-01 00:24:37.924739
# Keep-alive comment: 2025-07-01 11:22:52.975807
# Keep-alive comment: 2025-07-01 22:22:57.265199
# Keep-alive comment: 2025-07-02 09:22:51.032294
# Keep-alive comment: 2025-07-02 20:24:40.098278
# Keep-alive comment: 2025-07-03 07:23:05.784796
# Keep-alive comment: 2025-07-03 18:22:31.409965
# Keep-alive comment: 2025-07-04 05:22:54.485604
# Keep-alive comment: 2025-07-04 16:22:50.874136
# Keep-alive comment: 2025-07-05 03:22:49.511905
# Keep-alive comment: 2025-07-05 14:22:54.546359
# Keep-alive comment: 2025-07-06 01:22:52.305745
# Keep-alive comment: 2025-07-06 12:22:49.306013
# Keep-alive comment: 2025-07-06 23:22:50.918278
# Keep-alive comment: 2025-07-07 10:22:51.483355
# Keep-alive comment: 2025-07-07 21:22:49.815444
# Keep-alive comment: 2025-07-08 08:22:54.816626
# Keep-alive comment: 2025-07-08 19:22:50.356639
# Keep-alive comment: 2025-07-09 06:23:01.520736
# Keep-alive comment: 2025-07-09 17:23:34.927637
# Keep-alive comment: 2025-07-10 04:22:50.098386
# Keep-alive comment: 2025-07-10 15:22:55.882068
# Keep-alive comment: 2025-07-11 02:22:48.881092
# Keep-alive comment: 2025-07-11 13:22:50.046064
# Keep-alive comment: 2025-07-12 00:22:36.191317
# Keep-alive comment: 2025-07-12 11:22:54.453948
# Keep-alive comment: 2025-07-12 22:22:50.471246
# Keep-alive comment: 2025-07-13 09:22:50.319028
# Keep-alive comment: 2025-07-13 20:22:35.050647
# Keep-alive comment: 2025-07-14 07:22:47.469899
# Keep-alive comment: 2025-07-14 18:23:10.540466
# Keep-alive comment: 2025-07-15 05:23:00.836358
# Keep-alive comment: 2025-07-15 16:22:55.325920
# Keep-alive comment: 2025-07-16 03:22:54.848794
# Keep-alive comment: 2025-07-16 14:22:55.652273
# Keep-alive comment: 2025-07-17 01:22:50.237431
# Keep-alive comment: 2025-07-17 12:22:56.552714
# Keep-alive comment: 2025-07-17 23:22:48.569712
# Keep-alive comment: 2025-07-18 10:23:10.377093
# Keep-alive comment: 2025-07-18 21:22:49.892539
# Keep-alive comment: 2025-07-19 08:23:30.305730
# Keep-alive comment: 2025-07-19 19:22:35.213244
# Keep-alive comment: 2025-07-20 06:22:59.600123
# Keep-alive comment: 2025-07-20 17:23:05.706877
# Keep-alive comment: 2025-07-21 04:23:00.158818
# Keep-alive comment: 2025-07-21 15:22:47.028102
# Keep-alive comment: 2025-07-22 02:23:09.529668
# Keep-alive comment: 2025-07-22 13:23:23.192015
# Keep-alive comment: 2025-07-23 00:22:56.620393
# Keep-alive comment: 2025-07-23 11:22:46.188280
# Keep-alive comment: 2025-07-23 22:22:49.544707
# Keep-alive comment: 2025-07-24 09:23:05.746132
# Keep-alive comment: 2025-07-24 20:22:51.537739
# Keep-alive comment: 2025-07-25 07:22:46.038938
# Keep-alive comment: 2025-07-25 18:22:51.183145
# Keep-alive comment: 2025-07-26 05:22:45.422984
# Keep-alive comment: 2025-07-26 16:22:50.207942
# Keep-alive comment: 2025-07-27 03:22:45.095917
# Keep-alive comment: 2025-07-27 14:22:35.767674
# Keep-alive comment: 2025-07-28 01:22:56.625810
# Keep-alive comment: 2025-07-28 12:22:51.744162
# Keep-alive comment: 2025-07-28 23:22:50.085110
# Keep-alive comment: 2025-07-29 10:22:25.493938
# Keep-alive comment: 2025-07-29 21:22:55.907367
# Keep-alive comment: 2025-07-30 08:22:52.024512
# Keep-alive comment: 2025-07-30 19:23:00.311243
# Keep-alive comment: 2025-07-31 06:23:05.315787
# Keep-alive comment: 2025-07-31 17:22:51.216396
# Keep-alive comment: 2025-08-01 04:22:48.998038
# Keep-alive comment: 2025-08-01 15:23:00.353051
# Keep-alive comment: 2025-08-02 02:22:44.636342
# Keep-alive comment: 2025-08-02 13:22:55.257858
# Keep-alive comment: 2025-08-03 00:22:50.967590
# Keep-alive comment: 2025-08-03 11:22:56.042136
# Keep-alive comment: 2025-08-03 22:22:50.597165
# Keep-alive comment: 2025-08-04 09:22:47.454386
# Keep-alive comment: 2025-08-04 20:22:52.104346
# Keep-alive comment: 2025-08-05 07:22:54.778591
# Keep-alive comment: 2025-08-05 18:22:56.037331
# Keep-alive comment: 2025-08-06 05:22:50.274902
# Keep-alive comment: 2025-08-06 16:24:41.276338
# Keep-alive comment: 2025-08-07 03:22:54.777108
# Keep-alive comment: 2025-08-07 14:22:56.738322
# Keep-alive comment: 2025-08-08 01:22:45.581059
# Keep-alive comment: 2025-08-08 12:22:56.374783
# Keep-alive comment: 2025-08-08 23:22:56.778374
# Keep-alive comment: 2025-08-09 10:22:49.959905
# Keep-alive comment: 2025-08-09 21:23:12.339415
# Keep-alive comment: 2025-08-10 08:22:56.496515
# Keep-alive comment: 2025-08-10 19:22:56.461788
# Keep-alive comment: 2025-08-11 06:22:50.880232
# Keep-alive comment: 2025-08-11 17:22:56.493883
# Keep-alive comment: 2025-08-12 04:22:55.305095
# Keep-alive comment: 2025-08-12 15:22:47.787538
# Keep-alive comment: 2025-08-13 02:22:56.285195
# Keep-alive comment: 2025-08-13 13:22:53.023704
# Keep-alive comment: 2025-08-14 00:22:49.454854
# Keep-alive comment: 2025-08-14 11:22:57.632639
# Keep-alive comment: 2025-08-14 22:22:50.706721
# Keep-alive comment: 2025-08-15 09:22:50.650965
# Keep-alive comment: 2025-08-15 20:22:39.984357
# Keep-alive comment: 2025-08-16 07:23:04.701108
# Keep-alive comment: 2025-08-16 18:22:50.943832
# Keep-alive comment: 2025-08-17 05:22:54.159828
# Keep-alive comment: 2025-08-17 16:22:49.335746
# Keep-alive comment: 2025-08-18 03:22:51.150109
# Keep-alive comment: 2025-08-18 14:22:52.255527
# Keep-alive comment: 2025-08-19 01:22:51.146427
# Keep-alive comment: 2025-08-19 12:22:56.714433
# Keep-alive comment: 2025-08-19 23:23:18.236128
# Keep-alive comment: 2025-08-20 10:22:53.002530
# Keep-alive comment: 2025-08-20 21:22:55.917237
# Keep-alive comment: 2025-08-21 08:22:52.595688
# Keep-alive comment: 2025-08-21 19:22:56.808120
# Keep-alive comment: 2025-08-22 06:22:56.106682
# Keep-alive comment: 2025-08-22 17:22:51.353434
# Keep-alive comment: 2025-08-23 04:23:00.455268
# Keep-alive comment: 2025-08-23 15:22:49.654693
# Keep-alive comment: 2025-08-24 02:22:49.748350
# Keep-alive comment: 2025-08-24 13:22:50.610767
# Keep-alive comment: 2025-08-25 00:22:57.016658
# Keep-alive comment: 2025-08-25 11:22:56.148472
# Keep-alive comment: 2025-08-25 22:22:50.956773
# Keep-alive comment: 2025-08-26 09:22:51.967383
# Keep-alive comment: 2025-08-26 20:22:56.225590
# Keep-alive comment: 2025-08-27 07:23:00.958128
# Keep-alive comment: 2025-08-27 18:22:31.079512
# Keep-alive comment: 2025-08-28 05:23:01.492343
# Keep-alive comment: 2025-08-28 16:22:51.454639
# Keep-alive comment: 2025-08-29 03:22:35.157243
# Keep-alive comment: 2025-08-29 14:22:41.663259
# Keep-alive comment: 2025-08-30 01:22:40.229899
# Keep-alive comment: 2025-08-30 12:22:35.927276
# Keep-alive comment: 2025-08-30 23:22:39.339473
# Keep-alive comment: 2025-08-31 10:22:35.504444
# Keep-alive comment: 2025-08-31 21:22:46.708524
# Keep-alive comment: 2025-09-01 08:22:49.822549
# Keep-alive comment: 2025-09-01 19:22:46.933861
# Keep-alive comment: 2025-09-02 06:22:35.557246
# Keep-alive comment: 2025-09-02 17:22:46.943877
# Keep-alive comment: 2025-09-03 04:22:39.556613
# Keep-alive comment: 2025-09-03 15:22:42.367484
# Keep-alive comment: 2025-09-04 02:22:44.713397
# Keep-alive comment: 2025-09-04 13:22:54.007309
# Keep-alive comment: 2025-09-05 00:22:35.833441
# Keep-alive comment: 2025-09-05 11:22:31.116666
# Keep-alive comment: 2025-09-05 22:22:40.532495
# Keep-alive comment: 2025-09-06 09:22:36.546293
# Keep-alive comment: 2025-09-06 20:22:35.740362
# Keep-alive comment: 2025-09-07 07:22:41.406581
# Keep-alive comment: 2025-09-07 18:22:41.413963
# Keep-alive comment: 2025-09-08 05:22:37.320051
# Keep-alive comment: 2025-09-08 16:22:42.446835
# Keep-alive comment: 2025-09-09 03:23:07.373072
# Keep-alive comment: 2025-09-09 14:22:42.784482
# Keep-alive comment: 2025-09-10 01:22:35.060645
# Keep-alive comment: 2025-09-10 12:22:47.253912
# Keep-alive comment: 2025-09-10 23:22:35.987350
# Keep-alive comment: 2025-09-11 10:22:38.639374
# Keep-alive comment: 2025-09-11 21:22:36.284069
# Keep-alive comment: 2025-09-12 08:22:50.956483
# Keep-alive comment: 2025-09-12 19:22:41.267069
# Keep-alive comment: 2025-09-13 06:22:29.569270
# Keep-alive comment: 2025-09-13 17:22:36.163420
# Keep-alive comment: 2025-09-14 04:22:26.277623
# Keep-alive comment: 2025-09-14 15:22:37.562275
# Keep-alive comment: 2025-09-15 02:22:35.132994
# Keep-alive comment: 2025-09-15 13:22:37.978279
# Keep-alive comment: 2025-09-16 00:22:36.333558
# Keep-alive comment: 2025-09-16 11:22:41.753864
# Keep-alive comment: 2025-09-16 22:22:35.211087
# Keep-alive comment: 2025-09-17 09:22:37.961818
# Keep-alive comment: 2025-09-17 20:22:47.240078
# Keep-alive comment: 2025-09-18 07:22:43.458051
# Keep-alive comment: 2025-09-18 18:22:42.863089
# Keep-alive comment: 2025-09-19 05:22:37.159658
# Keep-alive comment: 2025-09-19 16:23:11.741598
# Keep-alive comment: 2025-09-20 03:22:40.874859
# Keep-alive comment: 2025-09-20 14:22:42.257603
# Keep-alive comment: 2025-09-21 01:22:41.930582
# Keep-alive comment: 2025-09-21 12:22:41.553902
# Keep-alive comment: 2025-09-21 23:22:36.900084
# Keep-alive comment: 2025-09-22 10:22:39.421777
# Keep-alive comment: 2025-09-22 21:22:36.161399
# Keep-alive comment: 2025-09-23 08:22:38.789010
# Keep-alive comment: 2025-09-23 19:22:43.751733
# Keep-alive comment: 2025-09-24 06:22:37.233520
# Keep-alive comment: 2025-09-24 17:22:43.118908
# Keep-alive comment: 2025-09-25 04:24:54.697718
# Keep-alive comment: 2025-09-25 15:22:47.107699
# Keep-alive comment: 2025-09-26 02:22:42.911712
# Keep-alive comment: 2025-09-26 13:22:46.627809
# Keep-alive comment: 2025-09-26 19:31:13.728195
# Keep-alive comment: 2025-09-27 05:31:18.981837
# Keep-alive comment: 2025-09-27 15:31:13.638009
# Keep-alive comment: 2025-09-28 01:31:17.974869
# Keep-alive comment: 2025-09-28 11:31:19.394208
# Keep-alive comment: 2025-09-28 21:31:17.855808
# Keep-alive comment: 2025-09-29 07:31:24.959790
# Keep-alive comment: 2025-09-29 17:31:34.362730
# Keep-alive comment: 2025-09-30 03:31:12.756010
# Keep-alive comment: 2025-09-30 13:31:19.665299
# Keep-alive comment: 2025-09-30 23:31:37.967823
# Keep-alive comment: 2025-10-01 09:31:44.755555
# Keep-alive comment: 2025-10-01 19:31:19.178192
# Keep-alive comment: 2025-10-02 05:31:47.134102
# Keep-alive comment: 2025-10-02 15:31:44.741414
# Keep-alive comment: 2025-10-03 01:31:18.228314
# Keep-alive comment: 2025-10-03 11:31:39.217903
# Keep-alive comment: 2025-10-03 21:31:13.519228
# Keep-alive comment: 2025-10-04 07:31:13.422177
# Keep-alive comment: 2025-10-04 17:31:23.296617
# Keep-alive comment: 2025-10-05 03:31:17.615669
# Keep-alive comment: 2025-10-05 13:31:23.010695
# Keep-alive comment: 2025-10-05 23:31:43.471413
# Keep-alive comment: 2025-10-06 09:31:49.307770
# Keep-alive comment: 2025-10-06 19:31:21.553242
# Keep-alive comment: 2025-10-07 05:31:20.483723
# Keep-alive comment: 2025-10-07 15:31:41.847797
# Keep-alive comment: 2025-10-08 01:31:18.689989
# Keep-alive comment: 2025-10-08 11:31:20.321291
# Keep-alive comment: 2025-10-08 21:31:19.499906
# Keep-alive comment: 2025-10-09 07:31:22.529575
# Keep-alive comment: 2025-10-09 17:31:22.002433
# Keep-alive comment: 2025-10-10 03:31:08.985003
# Keep-alive comment: 2025-10-10 13:31:00.888577
# Keep-alive comment: 2025-10-10 23:31:13.367207
# Keep-alive comment: 2025-10-11 09:31:19.462195
# Keep-alive comment: 2025-10-11 19:31:12.935407
# Keep-alive comment: 2025-10-12 05:31:16.569027
# Keep-alive comment: 2025-10-12 15:31:21.348514
# Keep-alive comment: 2025-10-13 01:31:15.122858
# Keep-alive comment: 2025-10-13 11:31:46.964103
# Keep-alive comment: 2025-10-13 21:31:09.567909
# Keep-alive comment: 2025-10-14 07:31:13.761951
# Keep-alive comment: 2025-10-14 17:31:16.744434
# Keep-alive comment: 2025-10-15 03:31:13.699450
# Keep-alive comment: 2025-10-15 13:31:16.109258
# Keep-alive comment: 2025-10-15 23:31:19.790919
# Keep-alive comment: 2025-10-16 09:31:15.896547
# Keep-alive comment: 2025-10-16 19:31:21.586246
# Keep-alive comment: 2025-10-17 05:31:20.085455
# Keep-alive comment: 2025-10-17 15:31:36.931508
# Keep-alive comment: 2025-10-18 01:31:15.070840
# Keep-alive comment: 2025-10-18 11:31:39.366868
# Keep-alive comment: 2025-10-18 21:31:49.065466
# Keep-alive comment: 2025-10-19 07:31:09.154443
# Keep-alive comment: 2025-10-19 17:31:44.082556
# Keep-alive comment: 2025-10-20 03:31:42.535743
# Keep-alive comment: 2025-10-20 13:31:21.036865
# Keep-alive comment: 2025-10-20 23:31:14.763789
# Keep-alive comment: 2025-10-21 09:31:20.766000
# Keep-alive comment: 2025-10-21 19:33:21.968946
# Keep-alive comment: 2025-10-22 05:31:15.840109
# Keep-alive comment: 2025-10-22 15:32:21.151853
# Keep-alive comment: 2025-10-23 01:31:14.081564
# Keep-alive comment: 2025-10-23 11:31:27.316599
# Keep-alive comment: 2025-10-23 21:31:16.573245
# Keep-alive comment: 2025-10-24 07:32:35.692620
# Keep-alive comment: 2025-10-24 17:31:25.825684
# Keep-alive comment: 2025-10-25 03:31:19.626566
# Keep-alive comment: 2025-10-25 13:31:43.456067
# Keep-alive comment: 2025-10-25 23:31:15.765068
# Keep-alive comment: 2025-10-26 09:31:08.775471
# Keep-alive comment: 2025-10-26 19:31:45.711102
# Keep-alive comment: 2025-10-27 05:31:26.167126
# Keep-alive comment: 2025-10-27 15:31:41.748316
# Keep-alive comment: 2025-10-28 01:31:18.560099
# Keep-alive comment: 2025-10-28 11:31:21.014470
# Keep-alive comment: 2025-10-28 21:31:09.519136
# Keep-alive comment: 2025-10-29 07:31:16.299216
# Keep-alive comment: 2025-10-29 17:31:25.517009
# Keep-alive comment: 2025-10-30 03:31:15.543903
# Keep-alive comment: 2025-10-30 13:31:46.759985
# Keep-alive comment: 2025-10-30 23:31:21.109510
# Keep-alive comment: 2025-10-31 09:32:35.491024
# Keep-alive comment: 2025-10-31 19:31:10.562303
# Keep-alive comment: 2025-11-01 05:31:19.344434
# Keep-alive comment: 2025-11-01 15:31:08.105248
# Keep-alive comment: 2025-11-02 01:31:20.270702
# Keep-alive comment: 2025-11-02 11:31:21.536808
# Keep-alive comment: 2025-11-02 21:31:35.538178
# Keep-alive comment: 2025-11-03 07:31:16.548635
# Keep-alive comment: 2025-11-03 17:31:21.773251
# Keep-alive comment: 2025-11-04 03:31:19.913791
# Keep-alive comment: 2025-11-04 13:31:47.597528
# Keep-alive comment: 2025-11-04 23:31:39.745201
# Keep-alive comment: 2025-11-05 09:31:51.118773
# Keep-alive comment: 2025-11-05 19:31:20.705316
# Keep-alive comment: 2025-11-06 05:31:45.629840
# Keep-alive comment: 2025-11-06 15:31:33.609444
# Keep-alive comment: 2025-11-07 01:31:18.432335
# Keep-alive comment: 2025-11-07 11:31:23.415420
# Keep-alive comment: 2025-11-07 21:31:22.052869
# Keep-alive comment: 2025-11-08 07:31:09.402260
# Keep-alive comment: 2025-11-08 17:31:25.319646
# Keep-alive comment: 2025-11-09 03:31:59.347937
# Keep-alive comment: 2025-11-09 13:31:20.590836
# Keep-alive comment: 2025-11-09 23:31:10.689101
# Keep-alive comment: 2025-11-10 09:31:17.363279
# Keep-alive comment: 2025-11-10 19:31:32.454006
# Keep-alive comment: 2025-11-11 05:31:17.236321
# Keep-alive comment: 2025-11-11 15:31:15.342590
# Keep-alive comment: 2025-11-12 01:31:22.278693
# Keep-alive comment: 2025-11-12 11:31:24.926425
# Keep-alive comment: 2025-11-12 21:31:42.181295
# Keep-alive comment: 2025-11-13 07:31:04.827995
# Keep-alive comment: 2025-11-13 17:31:16.944171
# Keep-alive comment: 2025-11-14 03:31:22.945364
# Keep-alive comment: 2025-11-14 13:31:44.212359
# Keep-alive comment: 2025-11-14 23:31:15.694743
# Keep-alive comment: 2025-11-15 09:31:19.565583
# Keep-alive comment: 2025-11-15 19:31:25.113925
# Keep-alive comment: 2025-11-16 05:31:16.520818
# Keep-alive comment: 2025-11-16 15:31:20.830854
# Keep-alive comment: 2025-11-17 01:31:11.207278
# Keep-alive comment: 2025-11-17 11:31:44.469972
# Keep-alive comment: 2025-11-17 21:31:13.024388
# Keep-alive comment: 2025-11-18 07:31:15.484925
# Keep-alive comment: 2025-11-18 17:31:16.258432
# Keep-alive comment: 2025-11-19 03:31:18.930710
# Keep-alive comment: 2025-11-19 13:31:12.016561
# Keep-alive comment: 2025-11-19 23:31:13.756464
# Keep-alive comment: 2025-11-20 09:31:21.074398
# Keep-alive comment: 2025-11-20 19:33:11.003507