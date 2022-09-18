import requests

import streamlit as st
import pandas as pd

API_KEY = 'YOUR API KEY'
base_url = 'https://api.covalenthq.com/v1'
aurora_chain_id = '1313161554'
demo_address = '0xb0bD02F6a392aF548bDf1CfAeE5dFa0EefcC8EaB'

def get_wallet_balance(chain_id, address):
    endpoint = f'/{chain_id}/address/{address}/balances_v2/?key=ckey_eb29565e970e4b46930dca374df'
    url = base_url + endpoint
    result = requests.get(url).json()
    data = result["data"]
    return(data)

def get_historical_portfolio(chain_id, address):
    endpoint = f'/{chain_id}/address/{address}/portfolio_v2/?key=ckey_eb29565e970e4b46930dca374df'
    url = base_url + endpoint
    result = requests.get(url).json()
    data = result["data"]['items'][0]['holdings']
    return(data)

def get_transactions(chain_id, address):
    endpoint = f'/{chain_id}/address/{address}/transactions_v2/?key=ckey_eb29565e970e4b46930dca374df'
    url = base_url + endpoint
    result = requests.get(url).json()
    data = result
    return(data)

def token_transfers(wallet, contract):
        url = f"https://api.covalenthq.com/v1/1/address/{wallet}/transfers_v2/?contract-address={contract}&key=ckey_eb29565e970e4b46930dca374df"
        response = requests.request("GET", url)
        if response.status_code ==200:
            data = response.json()
            data = data['data']['items']
            df = pd.DataFrame(data)
            return df
        else:
            st.info("Data Not Found")

def balance(address):
        url = f"https://api.covalenthq.com/v1/1/address/{address}/balances_v2/?quote-currency=USD&format=JSON&nft=false&no-nft-fetch=false&key=ckey_eb29565e970e4b46930dca374df"
        response = requests.request("GET", url)
        if response.status_code ==200:
            data = response.json()
            data = data['data']['items']
            df = pd.DataFrame(data)
            return df
        else:
            st.info("Data Not Found")



def get_nft_trans(address, token):
        url = f"https://api.covalenthq.com/v1/1/tokens/{address}/nft_transactions/{token}/?quote-currency=USD&format=JSON&key=ckey_eb29565e970e4b46930dca374df"
        response = requests.request("GET", url)
        if response.status_code ==200:
            data = response.json()
            data = data['data']['items']
            df = pd.DataFrame(data)
            return df
        else:
            st.info("Data Not Found")

def transaction_hash(hash):
        url = f"https://api.covalenthq.com/v1/1/transaction_v2/{hash}/?key=ckey_eb29565e970e4b46930dca374df"
        response = requests.request("GET", url)
        if response.status_code ==200:
            data = response.json()
            data = data['data']['items']
            df = pd.DataFrame(data)
            return df
        else:
            st.info("Data Not Found")


def topic_hash(hash, wallet):
        url = f"https://api.covalenthq.com/v1/1/events/topics/{hash}/?starting-block=12500000&ending-block=12500100&sender-address={wallet}&key=ckey_eb29565e970e4b46930dca374df"
        response = requests.request("GET", url)
        if response.status_code ==200:
            data = response.json()
            data = data['data']['items']
            df = pd.DataFrame(data)
            return df
        else:
            st.info("Data Not Found")

