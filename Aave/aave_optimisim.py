import requests
import plost
import datetime
import pandas as pd
from pathlib import Path
from sqlite3 import Connection
from common.connect import *
import streamlit as st



def aave_opti():
    
    st.markdown('#')

    data = connect('db/aave_optimisim.db')
    st.markdown("#")
    st.title("Aave_v3_Optimisim")

    st.markdown("#")

    col1, col2, col3 = st.columns((3,3,3))
    col1.metric("Today's Deposits volume", 7815276.21)
    col2.metric("Today's Depositors", 314)
    col3.metric("Today's Deposits", 1937)

    col1.metric("Today's Borrows volume", 5014518.23)
    col2.metric("Today's Borrows", 494)
    col3.metric("Today's Borrowers", 586)

    #line_chart(data, 'AAVE_V3_Polygon_Daily_New_User', 'min_dt', 'count', 'AAVE_V3_Polygon_Daily_New_User')
    line_chart_multi(data,'AAVE_V3_Optimism_Users_activity', 'dt', 'activer_users','account', 'AAVE_V3_Optimism_Users_activity')

    col1, col2 = st.columns((3,3))
    with col1:
        line_chart(data,'AAVE_V3_Optimism_Main_stats', 'day', 'TotalSupplied', 'AAVE_V3_Optimism_Total_Supplied')
        line_chart(data,'AAVE_V3_Optimism_Main_stats', 'day', 'TotalBorrowed', 'AAVE_V3_Optimism_Total Borrowed')
        line_chart(data,'AAVE_V3_Optimism_Main_stats', 'day', 'TotalAvailable', 'AAVE_V3_Optimism_TotalAvailable')
        line_chart_multi(data,'AAVE_V3_Optimism_Market_Overview', 'day', 'deposits','symbol', 'AAVE_V3_Optimism_depositors')
        line_chart_multi(data,'AAVE_V3_Optimism_Market_Overview', 'day', 'loans','symbol', 'AAVE_V3_Optimism_loans')
        line_chart_multi(data,'Aave_V3_Optimism_Loan_Volume_By_Token_Amount', 'day', 'usd_value','token', 'Aave_V3_Optimism_Loan_Volume_By_Token_Amount')
        line_chart(data,'Aave_V3_Optimism_New_Existing_Wallets', 'time', 'active_wallets', 'Aave_V3_Optimism_Active_Wallets')
       
    with col2:
        line_chart_multi(data,'AAVE_V3_Optimism_Main_stats_by_token', 'day', 'TotalSupplied','token', 'AAVE_V3_Optimism_Total_Supplied')
        line_chart_multi(data,'AAVE_V3_Optimism_Main_stats_by_token', 'day', 'TotalBorrowed','token', 'AAVE_V3_Optimism_Total Borrowed')
        line_chart_multi(data,'AAVE_V3_Optimism_Main_stats_by_token', 'day', 'TotalAvailable','token', 'AAVE_V3_Optimism_TotalAvailable')
        line_chart_multi(data,'AAVE_V3_Optimism_Borrow_Rates', 'time', 'stable_rate','symbol', 'AAVE_V3_Optimism_Borrow_Rates')
        line_chart(data,'Aave_V3_Optimism_Borrowers_Depositors_Transactions', 'date', 'borrowers','Aave_V3_Optimism_Borrowers')
        line_chart(data,'Aave_V3_Optimism_Borrowers_Depositors_Transactions', 'date', 'depositors','Aave_V3_Optimism_Depositors')
        line_chart(data,'Aave_V3_Optimism_Borrowers_Depositors_Transactions', 'date', 'total_transactions','Aave_V3_Optimism_Total_Transactions')
    
    line_chart(data,'Aave_V3_Optimism_New_Existing_Wallets', 'time', 'existing_wallets', 'Aave_V3_Optimism_Existing_Wallets')
    line_chart(data,'Aave_V3_Optimism_New_Existing_Wallets', 'time', 'new_unique_wallets', 'Aave_V3_Optimism_New_Unique_Wallets')