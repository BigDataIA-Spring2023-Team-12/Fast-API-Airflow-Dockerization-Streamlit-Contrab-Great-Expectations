import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# st.set_page_config(
#     page_title="Hello",
#     page_icon="🛰",
# )

st.write("# Nexrad Locations in USA 📍")
df = pd.read_csv('./nexrad_loc.csv')
df['text'] = 'City: ' + df['City'] + ', ' + 'State: '+ df["State"] + ', ' + 'Identifier: ' + df['ICAO Location Identifier'].astype(str)



fig = go.Figure(data=go.Scattergeo(
        lon = df['Long'],
        lat = df['Lat'],
        text = df['text'],
        mode = 'markers',
        ))

fig.update_layout(
        title = 'NexRad Locations',
        geo_scope='usa',
        geo = dict(bgcolor= 'rgba(0,0,0,0)',
                    lakecolor='#4E5D6C',
                    landcolor='rgba(51,17,0,0.2)',
                    subunitcolor='grey'),
        
    )
st.plotly_chart(fig, use_container_width=True)





