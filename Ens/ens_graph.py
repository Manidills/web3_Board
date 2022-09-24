from common.csv import download_csv
import streamlit as st
import requests

def iterate_val(value):
    it = iter(value)

    col1, col2 = st.columns((2,2))

    for i in it:
        with col1:
            st.write(i)
        with col2:
            try:
                st.write(next(it))
            except:
                pass

def multiple_value(query, key_val):
    with st.form("form1", clear_on_submit=False): 
                col1, col2 = st.columns((2,2))
                with col1:
                        val = st.radio(
                        'Limit',
                        (10,20,100))
                if key_val == 'delegates':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('numberVotes', 'id', 'delegatedVotes'))
                elif key_val == 'tokenHolders':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('tokenBalance', 'id', 'totalTokensHeld'))
                elif key_val == 'governances':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('totalTokenSupply', 'id', 'totalDelegates'))



                submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "query": query % (val, order_),
        }
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/messari/ens-governance',
                            json=payload).json()
        list_of_values = res['data'][key_val]
        iterate_val(list_of_values)
        download_csv(res['data'][key_val])

def single_value(query):
    with st.form("form1", clear_on_submit=False): 
                
                val = st.text_input("Enter ID")


                submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "query": query % (str(val)),
        }
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/messari/ens-governance',
                            json=payload).json()
        st.write(res)
        download_csv(res)

def ens_graph():
        ens_manage = st.radio(
            'ENS Governance',
            ('Top_Delegates', 'Delegate', 'Top_tokenHolders', 'TokenHolder', 'Governances'),horizontal=True)
        
        if ens_manage == 'Top_Delegates':

           
                    query = """{ 
                         delegates(first: %s, orderBy: %s, orderDirection: desc) {
                            delegatedVotes
                            delegatedVotesRaw
                            id
                            numberVotes
                            tokenHoldersRepresentedAmount
                        } }"""
                    multiple_value(query,'delegates')
                    
        elif ens_manage == 'Delegate':
           
                    query =  """{ 
                            delegate(id: \"%s\") {
                            delegatedVotes
                            delegatedVotesRaw
                            id
                            numberVotes
                            tokenHoldersRepresentedAmount
                        } }""" 
                    single_value(query)
        elif ens_manage == 'Top_tokenHolders':
                    query = """{
                        tokenHolders(
                        first: %s
                        orderBy: %s
                        orderDirection: desc
                        skip: 10
                        subgraphError: allow
                    ) {
                        id
                        tokenBalance
                        tokenBalanceRaw
                        totalTokensHeld
                        totalTokensHeldRaw
                    }
                    }"""
                    multiple_value(query,'tokenHolders')
        elif ens_manage == 'TokenHolder':
                    query= """{

                         tokenHolder(id:  \"%s\") {
                            id
                            tokenBalance
                            tokenBalanceRaw
                            totalTokensHeld
                            totalTokensHeldRaw
                            delegate {
                            delegatedVotes
                            delegatedVotesRaw
                            numberVotes
                            tokenHoldersRepresentedAmount
                            }
                        }
                    }"""
                    single_value(query)
        elif ens_manage == 'Governances':
                    query = """{
                            governances(first: %s, orderBy: %s, orderDirection: desc) {
                            currentDelegates
                            currentTokenHolders
                            delegatedVotes
                            delegatedVotesRaw
                            id
                            proposals
                            proposalsCanceled
                            proposalsExecuted
                            proposalsQueued
                            totalDelegates
                            totalTokenHolders
                        }
                    }"""
                    
                    multiple_value(query,'governances')

                   