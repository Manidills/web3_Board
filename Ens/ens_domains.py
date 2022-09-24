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
                if key_val == 'enss':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('cost', 'expires', 'id'))


                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                       "query": query % (val,order_),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/salmandabbakuti/ens-registry',
                                        json=payload).json()
                    list_of_values = res['data'][key_val]
                    iterate_val(list_of_values)

def single_value(query):
    with st.form("form1", clear_on_submit=False): 
                
                val = st.text_input("Enter Top Level Domain")


                submit = st.form_submit_button("Submit")

                if submit:
                    payload = {
                        "query": query % (str(val)),
                    }
                    res = requests.post(url='https://api.thegraph.com/subgraphs/name/salmandabbakuti/ens-registry',
                                        json=payload).json()
                    st.write(res)

def ens_domains():
        ens_manage = st.radio(
            'ENS Domains',
            ('Top_Level_Domains_By_Cost','Top_Level_Domain'),horizontal=True)
        
        if ens_manage == 'Top_Level_Domains_By_Cost':

           
                    query = """{ 
                         enss(first: %s, orderBy: %s, orderDirection: desc) {
                            cost
                            expires
                            id
                            label
                            name
                            owner
                            updatedAt
                        }
                         }"""
                    multiple_value(query,'enss')
                    
        elif ens_manage == 'Top_Level_Domain':
           
                    query =  """{ 
                            ens(id: \"%s\") {
                                cost
                                expires
                                id
                                label
                                name
                                owner
                                updatedAt
                            }
                            }""" 
                    single_value(query)
        elif ens_manage == 'Top_tokenHolders':
                    query = """{
                        tokenHolders(
                        first: %s
                        orderBy: tokenBalance
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
                            governances(first: %s, orderBy: currentTokenHolders, orderDirection: desc) {
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

                   