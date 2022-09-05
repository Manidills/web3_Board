import requests
import plost
import datetime
import pandas as pd
from pathlib import Path
from sqlite3 import Connection
from common.connect import *
import streamlit as st



def yearn():
    
    st.markdown('#')

    data = connect('db/yearn.db')
    st.markdown("#")
    st.title("Yearn Vaults")

    st.markdown("#")
    st.subheader("Trending_Vaults_2022")
    st.dataframe(table(data, 'Trending_Vaults_2022'))

    st.markdown("#")
    st.subheader("Y_Vault_Correlation")
    st.dataframe(table(data, 'Y_Vault_Correlation'))

    line_chart(data, 'Yearn_Vault_Users', 'date', 'REPEAT USERS DAILY', 'Yearn_Vault_Repeated_Users')
    line_chart(data, 'Yearn_Vault_Users', 'date', 'TOTAL USERS DAILY', 'Yearn_Vault_Total_Users')
    line_chart(data, 'Yearn_Vault_Users', 'date', 'UNIQUE USERS DAILY', 'Yearn_Vault_UNIQUE_Users')

    col1,col2 = st.columns((2,3))


    with col1:
        st.subheader('Y_Top_Correlated_Vault_Pairs')
        st.dataframe(table(data, 'Y_Top_Correlated_Vault_Pairs_Occurrence_in_Wallets'))
        
        
        
    with col2:
        st.subheader('Y_Top_Correlated_Vault_Trio')
        st.dataframe(table(data, 'Y_Top_Correlated_Vault_Trio_Occurrence_in_Wallets'))
       

    
    st.subheader('Yearn_yVault_User_Invested_Vaults_Array')
    st.dataframe(table(data, 'Yearn_yVault_User_Invested_Vaults_Array'))

    col1, col2 = st.columns((2,2))

    with col1:
        line_chart(data, 'Yearn_DAI_yVault','date', 'Vault $TVL', 'Yearn_DAI_yVault_TVL')
        line_chart(data, 'Yearn_stEth_Pool','date', 'Vault $TVL', 'Yearn_stEth_yVault_TVL')
        line_chart(data, 'Yearn_yvUSDC_Pool_Metrics','date', 'Vault $TVL', 'Yearn_yvUSDC_yVault_TVL')

    with col2:
        line_chart(data, 'Yearn_WETH_yVault_Metrics','date', 'TVL', 'Yearn_WETH_yVault_TVL')
        line_chart(data, 'Yearn_WETH_yVault_Metrics','date', 'Cumulative Deposits', 'Yearn_DAI_yVault_Avg_deposits')
        line_chart(data, 'Yearn_WETH_yVault_Metrics','date', 'Cumulative Withdrawals', 'Yearn_DAI_yVault_Avg_withdraw')

    st.subheader("Yearn_yVault_Yearly_Returns")
    st.dataframe(table(data,'Yearn_yVault_Yearly_Returns'))


    col1, col2 = st.columns((2,2))

    with col1:

        st.subheader('Yearn_Vault_First_Deposit_Time')
        st.dataframe(table(data, 'Yearn_Vault_First_Deposit_Time'))
    with col2:
        st.subheader('iearn_v2_Deployments')
        st.dataframe(table(data, 'iearn_v2_Deployments'))
  

   