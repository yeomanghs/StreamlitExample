#import modules
import streamlit as st
import pandas as pd
import pathlib

#predefine parameters
#current working dir
wd = str(pathlib.Path().absolute())
resultFileName = "tempResult"

#widget to upload file
file = st.file_uploader("Upload file", type = ['csv', 'xlsx'])

#function to read file
@st.cache(suppress_st_warning = True)
def load_data(file_uploaded):
    if '.xlsx' in file_uploaded.name:
        return pd.read_excel(file_uploaded, sep=',', encoding='utf-8')
    elif '.csv' in file_uploaded.name:
        return pd.read_csv(file_uploaded, sep=',', encoding='utf-8')

#if file is uploaded
if file:
    st.markdown("Filename: %s"%file.name)
    st.markdown("Uploaded file: %s"%"YES")
    df = load_data(file)
    st.markdown("Number of rows: %s"%df.shape[0])

    #test data manipulation
    dfGrouped = df.groupby("Region")['client_id'].count().reset_index()

    if dfGrouped.shape[0]!=0:
        #download button
        button = st.button('Download Result', key = 'JN')
        resultLoc = wd + "\\" + resultFileName

        #if click download button
        if button:
            if '.xlsx' in file.name:
                resultLoc2 = resultLoc + '.xlsx'
                dfGrouped.to_excel(resultLoc2, index = False)
            elif '.csv' in file.name:
                resultLoc2 = resultLoc + '.csv'
                dfGrouped.to_csv(resultLoc2, index = False)
            #success msg
            st.markdown('Result is saved as %s' %resultLoc2)