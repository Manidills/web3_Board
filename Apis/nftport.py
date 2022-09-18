import json
import requests
import pandas as pd
import streamlit as st





def contract_stats(chain, address,):
    url = f"https://api.nftport.xyz/v0/transactions/stats/{address}"
    payload = {
        "chain": str(chain)
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:

        data = response.json()

        return data
    else:
        st.info("Data Not Found")

def contract_trans(chain, address):
    url = f"https://api.nftport.xyz/v0/transactions/nfts/{address}"
    payload = {
        "chain": str(chain),
        "type":"sale"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:

        data = response.json()
        data = data['transactions']
        df = pd.DataFrame(data)
        return df
    else:
        st.info("Data Not Found")

def nft_token(chain, address, token):
    url = f"https://api.nftport.xyz/v0/nfts/{address}/{token}"
    payload = {
        "chain": str(chain)
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:

        data = response.json()

        return data
    else:
        st.info("Data Not Found")


def nft_trans(chain, address, token):
    url = f"https://api.nftport.xyz/v0/transactions/nfts/{address}/{token}"
    payload = {
        "chain": str(chain),
        "type":"sale"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:

        data = response.json()
        data = data['transactions']
        df = pd.DataFrame(data)
        return df
    else:
        st.info("No Sales yet")

def wallet_nft_created(chain,address):
    url = f"https://api.nftport.xyz/v0/accounts/creators/{address}"
    payload = {
        "chain": str(chain),"include":"metadata"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:

        data = response.json()
        #st.write(data)
        #data = pd.DataFrame.from_dict(data['nfts'], orient='columns')
        return data
    else:
        st.info("Data Not Found")

def wallet_nft_owned(chain,address):
    url = f"https://api.nftport.xyz/v0/accounts/{address}"
    payload = {
        "chain": str(chain),"include":"metadata"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:
       
        data = response.json()
        try:
            data = data['nfts']
            
            return data
        except:
           st.info("Data Not Found")

        
    else:
        st.info("Data Not Found")

def wallet_contract_owned(chain,address):
    url = f"https://api.nftport.xyz/v0/accounts/contracts/{address}"
    payload = {
        "chain": str(chain),"type": "owns_contract_nfts"
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "f6ce3372-a928-4947-8f50-87649f60cee2"
        }

    response = requests.request("GET", url,  params=payload, headers=headers)
    if response.status_code ==200:
       
        data = response.json()
        data = data['contracts']
        df = pd.DataFrame(data)
        return df

        
    else:
        st.info("Data Not Found")

def dupliacte(chain,address,token):
    url = "https://api.nftport.xyz/v0/duplicates/tokens"

    payload = {
        "chain": str(chain),
        "contract_address": address,
        "token_id": token,
        "page_number": 1,
        "page_size": 1,
        "threshold": 0.9
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "f6ce3372-a928-4947-8f50-87649f60cee2"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return(response.json())
