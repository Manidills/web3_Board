from audioop import mul
from Apis.covalent import get_historical_portfolio, get_transactions, get_wallet_balance
from common.csv import download_csv
import streamlit as st
import requests
import web3

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
                with col2:
                    Sales_type = st.selectbox(
                    'Order By',
                    ('price', 'id'))


                submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "query": query % (val, Sales_type),
        }
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/superfluid-finance/protocol-v1-arbitrum-one',
                            json=payload).json()
        list_of_values = res['data'][key_val]
        iterate_val(list_of_values)
        download_csv(res['data'][key_val])

def multiple_value_dex(query, key_val):
    with st.form("form1", clear_on_submit=False): 
                col1, col2 = st.columns((2,2))
                with col1:
                    val = st.radio(
                    'Limit',
                    (10,20,100))
                # with col2:
                #     Sales_type = st.selectbox(
                #     'Order By',
                #     ('price', 'id'))


                submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "query": query % (val),
        }
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/superfluid-finance/protocol-v1-arbitrum-one',
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
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/superfluid-finance/protocol-v1-arbitrum-one',
                            json=payload).json()
        st.write(res)
        download_csv(res)


def superfluid_arbi():
        st.write("mani")
        xdai_manage = st.radio(
            'Superfluid_Xdai_Explorer',
            ('Accounts','MintedEvents','Top_flowUpdatedEvents', 'Top_tokenStatistics', 'TransferEvents', 'Streams', 'SuperTokenCreatedEvents'))
        
        if xdai_manage == 'Accounts':

                    query = """{ 
                        accounts(first: %s, orderBy: createdAtTimestamp, orderDirection: desc) {
                            createdAtBlockNumber
                            createdAtTimestamp
                            id
                            isSuperApp
                            updatedAtBlockNumber
                            updatedAtTimestamp
                        }
                        }"""
                    multiple_value_dex(query,'accounts')

        elif xdai_manage == 'Top_flowUpdatedEvents':

                query = """{ 
                        flowUpdatedEvents(first: %s, orderBy: flowRate, orderDirection: desc) {
                            addresses
                            blockNumber
                            deposit
                            flowOperator
                            flowRate
                            gasPrice
                            id
                            logIndex
                            name
                            oldFlowRate
                            order
                            receiver
                            sender
                            token
                            totalAmountStreamedUntilTimestamp
                            totalReceiverFlowRate
                            totalSenderFlowRate
                            transactionHash
                            type
                            userData
                        }
                        }"""
                multiple_value_dex(query,'flowUpdatedEvents')
        
        elif xdai_manage == 'Top_tokenStatistics':

                query = """{ 
                        tokenStatistics(
                            first: %s
                            orderBy: totalSupply
                            orderDirection: desc
                        ) {
                            id
                            totalAmountDistributedUntilUpdatedAt
                            totalAmountStreamedUntilUpdatedAt
                            totalAmountTransferredUntilUpdatedAt
                            totalApprovedSubscriptions
                            totalDeposit
                            totalNumberOfActiveIndexes
                            totalNumberOfActiveStreams
                            totalNumberOfClosedStreams
                            totalNumberOfIndexes
                            totalOutflowRate
                            totalSubscriptionsWithUnits
                            totalSupply
                            updatedAtBlockNumber
                            updatedAtTimestamp
                        }
                        }"""
                multiple_value_dex(query,'tokenStatistics')
        
        elif xdai_manage == 'TransferEvents':

                query = """{ 
                       transferEvents(first: %s, orderBy: id) {
                            addresses
                            blockNumber
                            gasPrice
                            id
                            logIndex
                            name
                            order
                            timestamp
                            token
                            transactionHash
                            value
                            to {
                            id
                            }
                            from {
                            id
                            }
                        }
                        }"""
                multiple_value_dex(query,'transferEvents')
        
        elif xdai_manage == 'Streams':

                query = """{ 
                        streams(first: %s, orderBy: deposit, orderDirection: desc) {
                            createdAtBlockNumber
                            createdAtTimestamp
                            currentFlowRate
                            deposit
                            id
                            streamedUntilUpdatedAt
                            updatedAtBlockNumber
                            updatedAtTimestamp
                        }
                        }"""
                multiple_value_dex(query,'streams')
        
        elif xdai_manage == 'MintedEvents':

                query = """{ 
                        mintedEvents(first: %s, orderBy: amount, orderDirection: desc, skip: 10) {
                        addresses
                        amount
                        blockNumber
                        data
                        gasPrice
                        id
                        logIndex
                        name
                        operator
                        operatorData
                        order
                        timestamp
                        to
                        token
                        transactionHash
                    }
                        }"""
                multiple_value_dex(query,'mintedEvents')
        
        elif xdai_manage == 'SuperTokenCreatedEvents':

                query = """{ 
                        superTokenCreatedEvents(first: %s, orderBy: gasPrice, orderDirection: desc, skip: 10) {
                            addresses
                            blockNumber
                            gasPrice
                            id
                            logIndex
                            name
                            order
                            timestamp
                            token
                            transactionHash
                        }
                        }"""
                multiple_value_dex(query,'superTokenCreatedEvents')
        
        