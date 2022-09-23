import requests
from Ens.ens_checks import lookup
from Ens.ens_domains import ens_domains
from Ens.ens_graph import ens_graph
from Ens.ens_status import status_check
import plost
import datetime
import pandas as pd
from pathlib import Path
from sqlite3 import Connection
from common.connect import *
import streamlit as st


def ens_charts():
    
    st.markdown('#')

    data = connect('db/ens.db')
    st.markdown("#")
    st.title("ENS")

    options_skale = st.radio(
    'Explorer',
    ('ENS_Analysis', 'ENS_Governance', 'Domain_Check', 'ENS_Status', 'Ens_Top_Level_Domains'),horizontal=True)

    st.markdown("#")
    
    if options_skale == 'ENS_Analysis':
        col1, col2, col3 = st.columns((3,3,3))
        col1.metric("otal ENS names created", 2494903)
        col2.metric("All ENS participating addresses", 564913)
        col3.metric("Primary names registered", 402107)

        line_chart(data, 'ens_growth', 'day', 'eth_growth', '.ETH_Total_Growth')
        line_chart(data, 'ens_growth', 'day', 'new_eth_users', '.ETH_New_Users_Growth')

        col1,col2 = st.columns((2,2))
        with col1:
            line_chart(data, 'ens_Avatar_record_growth', 'date_trunc', 'count', 'Ens_Avatar_Record_Growth')
            line_chart(data, 'ens_daily_registration', 'day', 'registration cost usd', 'Ens_daily_registration_cost')
            line_chart(data, 'ens_daily_registration', 'day', 'registration count', 'Ens_daily_registration_count')
            st.subheader("Whales")
            st.dataframe(table(data, 'ens_eth_domain_whales'))
        with col2:
            line_chart(data, 'ens_name_trading_volume', 'date_trunc', 'sum_usd', 'Ens_name_trading_volume')
            line_chart(data, 'ens_name_trading_volume', 'date_trunc', 'count', 'Ens_name_trading_count')
            line_chart(data, 'ens_growth', 'day', 'renewal ratio (%)', '.ETH_Renewal_Ratio_Percentage')
            st.subheader("Ens_trading_volume_by_platform")
            st.dataframe(table(data, 'ens_trading_volume_by_platform'))

    elif options_skale == 'ENS_Governance':
        ens_graph()
    elif options_skale == 'Domain_Check':
        status_check()
    elif options_skale == 'ENS_Status':
        lookup()
    elif options_skale == 'Ens_Top_Level_Domains':
        ens_domains()

        