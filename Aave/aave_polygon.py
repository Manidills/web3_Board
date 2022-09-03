import requests
import plost
import datetime
import pandas as pd
from pathlib import Path
from sqlite3 import Connection
from common.connect import *
import streamlit as st



def aave_poly():
    
    st.markdown('#')

    data = connect('db/aave_polygon.db')
    st.markdown("#")
    st.title("Aave_v3 Polygon")

    st.markdown("#")

    line_chart(data, 'AAVE_V3_Polygon_Daily_New_User', 'min_dt', 'count', 'AAVE_V3_Polygon_Daily_New_User')

    st.markdown("#")
    line_chart_multi(data,'AAVE_V3_Polygon_Users_activity', 'dt', 'activer_users','account', 'AAVE_V3_Polygon_Users_activity')

    col1, col2 = st.columns((3,3))
    with col1:
        line_chart(data,'AAVE_V3_Polygon_Main_stats', 'day', 'TotalSupplied', 'AAVE_V3_Polygon_Total_Supplied')
        line_chart(data,'AAVE_V3_Polygon_Main_stats', 'day', 'TotalBorrowed', 'AAVE_V3_Polygon_Total Borrowed')
        line_chart(data,'AAVE_V3_Polygon_Main_stats', 'day', 'TotalAvailable', 'AAVE_V3_Polygon_TotalAvailable')
    with col2:
        line_chart_multi(data,'AAVE_V3_Polygon_Users_Every_Day', 'dt', 'active_users','account', 'AAVE_V3_Polygon_Active_Users')
        line_chart(data,'Aave_V3_Polygon_Borrowers_Depositors_Transactions', 'date', 'depositors', 'Aave_V3_Polygon_Depositers')
        line_chart(data,'Aave_V3_Polygon_Borrowers_Depositors_Transactions', 'date', 'borrowers', 'Aave_V3_Polygon_Borrowers')
    
    st.markdown("#")
    line_chart(data,'Aave_V3_Polygon_Borrowers_Depositors_Transactions', 'date', 'total_transactions', 'Aave_V3_Polygon_Total_Transactions')
    line_chart_multi(data,'Aave_V3_Polygon_Loan_Volume_By_Token_Amount', 'day', 'usd_value','token', 'Aave_V3_Polygon_Loan_Volume_By_Token_Amount')
   
    col1, col2 = st.columns((3,3))

    with col1:
        line_chart(data,'Aave_V3_Polygon_New_Existing_Wallets', 'time', 'new_unique_wallets', 'Aave_V3_Polygon_New_Unique_Wallets')
       
    with col2:
        line_chart(data,'Aave_V3_Polygon_New_Existing_Wallets', 'time', 'existing_wallets', 'Aave_V3_Polygon_Existing_Wallets')
        
       