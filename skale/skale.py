import requests
import plost
import datetime
import pandas as pd
from pathlib import Path
from sqlite3 import Connection
from common.connect import *
import streamlit as st


def skl():
    
    st.markdown('#')

    data = connect('db/skl.db')
    st.markdown("#")
    st.title("Skale")

    options_skale = st.radio(
    'Explorer',
    ('SKL', 'SKALE Manager'),horizontal=True)

    st.markdown("#")
    
    if options_skale == 'SKL':

        line_chart(data, 'skl_price', 'date', 'price', 'SKL_Price')
        line_chart(data, 'skl_users', 'date', 'total_users', 'SKL_users')
        line_chart(data, 'skl_transactiona', 'date', 'count', 'SKL_transactions')

        col1, col2 = st.columns((2,2))
        with col1:
            line_chart(data, 'skl_active_users', 'date', 'Old', 'SKL_active_users_old')
            line_chart(data, 'skl_average_users_per_day', 'time', 'avg_new', 'SKL_average_users_per_day')
        with col2:
            line_chart(data, 'skl_active_users', 'date', 'New', 'SKL_active_users_new')
            line_chart(data, 'skl_buys_on_dex', 'date', 'unique_wallet_count', 'SKL_buys_on_dex_unique_wallets')
        
        line_chart(data, 'skl_buys_on_dex', 'date', 'price_per_trade', 'SKL_buys_on_dex_price_per_trade')

        st.subheader("SKL_on_dex")
        st.dataframe(table(data, 'skl_buys_on_dex'))

    elif options_skale == 'SKALE Manager':

        skl_manage = st.radio(
            'Subgraph_Explorer',
            ('Top_Validators(claimedFee)', 'Validator', 'Top_Delegators(claimedBounty)', 'Delegator', 'Top_Delegations(amount)', 'Delegation'),horizontal=True)
        
        if skl_manage == 'Top_Validators(claimedFee)':

            with st.form("form1", clear_on_submit=False): 
                col1, col2 = st.columns((2,2))
                with col1:
                    val = st.radio(
                    'Limit',
                    (10,20,100))

                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                        validators(first:  %s , orderBy: claimedFee, orderDirection: desc, skip: 10) {
                                acceptNewRequests
                                address
                                claimedFee
                                currentDelegationAmount
                                currentDelegationCount
                                description
                                feeRate
                                id
                                isEnabled
                                minimumDelegationAmount
                                name
                                registrationTime
                            } }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    list_of_values = res['data']['validators']
                    it = iter(list_of_values)

                    col1, col2 = st.columns((2,2))

                    for i in it:
                        with col1:
                            st.write(i)
                        with col2:
                            try:
                                st.write(next(it))
                            except:
                                pass
        elif skl_manage == 'Validator':
             with st.form("form1", clear_on_submit=False): 
                
                val = st.text_input("Enter ID")


                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                            validator(id: %s) {
                            acceptNewRequests
                            address
                            claimedFee
                            currentDelegationAmount
                            currentDelegationCount
                            description
                            feeRate
                            isEnabled
                            minimumDelegationAmount
                            name
                            registrationTime
                            requestedAddress
                            id
                        }
                       }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    st.write(res)

        elif skl_manage == 'Top_Delegators(claimedBounty)':
             with st.form("form", clear_on_submit=False): 
                col1, col2 = st.columns((2,2))
                with col1:
                    val = st.radio(
                    'Limit',
                    (10,20,100))

                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                            delegators(first: %s, orderBy: claimedBounty, orderDirection: desc) {
                                claimedBounty
                                currentAmount
                                currentCount
                                id
                            }

                         }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    list_of_values = res['data']['delegators']
                    it = iter(list_of_values)

                    col1, col2 = st.columns((2,2))

                    for i in it:
                        with col1:
                            st.write(i)
                        with col2:
                            try:
                                st.write(next(it))
                            except:
                                pass
        elif skl_manage == 'Delegator':
            with st.form("form1", clear_on_submit=False): 
                
                val = st.text_input("Enter Address")


                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                            delegator(id: \"%s\") {
                            claimedBounty
                            currentAmount
                            currentCount
                            id
                        }
                       }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    st.write(res)
        
        elif skl_manage == 'Top_Delegations(amount)':
             with st.form("form", clear_on_submit=False): 
                col1, col2 = st.columns((2,2))
                with col1:
                    val = st.radio(
                    'Limit',
                    (10,20,100))

                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                             delegations(first: %s, orderDirection: desc, orderBy: amount) {
                                amount
                                created
                                delegationPeriod
                                finished
                                id
                                info
                                started
                                state
                            }

                         }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    list_of_values = res['data']['delegations']
                    it = iter(list_of_values)

                    col1, col2 = st.columns((2,2))

                    for i in it:
                        with col1:
                            st.write(i)
                        with col2:
                            try:
                                st.write(next(it))
                            except:
                                pass
        
        
        elif skl_manage == 'Delegation':
            with st.form("form1", clear_on_submit=False): 
                
                val = st.text_input("Enter Address")


                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": """{ 
                            delegation(id: %s) {
                            amount
                            created
                            delegationPeriod
                            finished
                            id
                            info
                            started
                            state
                            holder {
                            claimedBounty
                            currentAmount
                            currentCount
                            }
                            delegatedBlock {
                            id
                            timestamp
                            }
                        }
                       }""" % (val),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/ministry-of-decentralization/skale-manager-subgraph',
                                        json=payload).json()
                    st.write(res)                