import streamlit as st # 1.11.0
import numpy as np
import pandas as pd
import time
import plotly.express as px
from datetime import datetime


df=pd.DataFrame()

#Dasboard Component
st.set_page_config(
    page_title='Real Sensor',
    layout='wide'
)
st.title("Real Time Sensor From Device")


room=['roomArea1', 'roomArea2', 'roomArea3']
room_filter = st.selectbox("Select room area", room)

placeholder = st.empty()

while True:
    
    with placeholder.container():

        temp = 20 + np.random.choice(range(1,500))/10
        hum = 80 + np.random.choice(range(1,500))/100
        timeNow = datetime.now()

        df_new = pd.DataFrame([[temp, hum, timeNow, 'roomArea1']], columns=['temperature', 'humidity', 'timestamp', 'roomNumber'])
        df = pd.concat([df, df_new])
        df_new = pd.DataFrame([[temp, hum, timeNow, 'roomArea2']], columns=['temperature', 'humidity', 'timestamp', 'roomNumber'])
        df = pd.concat([df, df_new])
        df_new = pd.DataFrame([[temp, hum, timeNow, 'roomArea3']], columns=['temperature', 'humidity', 'timestamp', 'roomNumber'])
        df = pd.concat([df, df_new])

        dfDisplay = df[df['roomNumber']==room_filter]

        #Temperatue
        dfTemp = dfDisplay[['timestamp', 'temperature']]
        dfTempMin = dfTemp.groupby([pd.Grouper(freq='15S', key='timestamp')]).min().reset_index()
        dfTempMin = dfTempMin.rename(columns={'temperature':'Min'})
        dfTempMax = dfTemp.groupby([pd.Grouper(freq='15S', key='timestamp')]).max().reset_index()
        dfTempMax = dfTempMax.rename(columns={'temperature':'Max'})
        dfTempMed = dfTemp.groupby([pd.Grouper(freq='15S', key='timestamp')]).median().reset_index()
        dfTempMed = dfTempMed.rename(columns={'temperature':'Med'})
        dfTempMean = dfTemp.groupby([pd.Grouper(freq='15S', key='timestamp')]).mean().reset_index()
        dfTempMean = dfTempMean.rename(columns={'temperature':'Mean'})
        dfTempNew = pd.merge(dfTempMin, dfTempMax, on='timestamp').merge(dfTempMed, on='timestamp').merge(dfTempMean, on='timestamp')

        #Humidity
        dfHum = dfDisplay[['timestamp', 'humidity']]
        dfHumMin = dfHum.groupby([pd.Grouper(freq='15S', key='timestamp')]).min().reset_index()
        dfHumMin = dfHumMin.rename(columns={'humidity':'Min'})
        dfHumMax = dfHum.groupby([pd.Grouper(freq='15S', key='timestamp')]).max().reset_index()
        dfHumMax = dfHumMax.rename(columns={'humidity':'Max'})
        dfHumMed = dfHum.groupby([pd.Grouper(freq='15S', key='timestamp')]).median().reset_index()
        dfHumMed = dfHumMed.rename(columns={'humidity':'Med'})
        dfHumMean = dfHum.groupby([pd.Grouper(freq='15S', key='timestamp')]).mean().reset_index()
        dfHumMean = dfHumMean.rename(columns={'humidity':'Mean'})
        dfHumNew = pd.merge(dfHumMin, dfHumMax, on='timestamp').merge(dfHumMed, on='timestamp').merge(dfHumMean, on='timestamp')

        temp_col, hum_col = st.columns(2)
        with temp_col:
            fig_temp = px.line(dfTempNew, x="timestamp", y=list(dfTempNew.keys()[1:]), title='Temperature')
            st.write(fig_temp)

        with hum_col:
            fig_hum = px.line(dfHumNew, x="timestamp", y=list(dfHumNew.keys()[1:]), title='Humidity')
            st.write(fig_hum)

        TMin, TMax, TMed, TMean,HMin, HMax, HMed, HMean = st.columns(8)

        TMin.metric(label="Temp Min : ", value=dfTempNew['Min'].iloc[-1])
        TMax.metric(label="Temp Max : ", value=dfTempNew['Max'].iloc[-1])
        TMed.metric(label="Temp Mad : ", value=dfTempNew['Med'].iloc[-1])
        TMean.metric(label="Temp Mean : ", value=dfTempNew['Mean'].iloc[-1])
        HMin.metric(label="Hum Min : ", value=dfHumNew['Min'].iloc[-1])
        HMax.metric(label="Hum Max : ", value=dfHumNew['Max'].iloc[-1])
        HMed.metric(label="Hum Mad : ", value=dfHumNew['Med'].iloc[-1])
        HMean.metric(label="Hum Mean : ", value=dfHumNew['Mean'].iloc[-1])
    time.sleep(1)
