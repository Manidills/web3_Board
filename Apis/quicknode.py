from web3 import Web3, HTTPProvider

def common_1():
    OPTIONS = {
    'headers':
        {
        'x-qn-api-version': '1'
        }
    }
    #https://sleek-prettiest-lambo.discover.quiknode.pro/d6ceca49553e531ff2c2ec0de06299c954e0c81e/
    w3 = Web3(HTTPProvider('https://sleek-prettiest-lambo.discover.quiknode.pro/d6ceca49553e531ff2c2ec0de06299c954e0c81e/', request_kwargs=OPTIONS))
    return w3


def token_metadata(contract):

    w3 = common_1()
    resp = w3.provider.make_request('qn_getTokenMetadataByContractAddress', {
    "contract": contract
    })
    return resp


def nft_contract_metadata(con):
   
    w3 = common_1()
    resp = w3.provider.make_request('qn_fetchNFTCollectionDetails', {
    "contracts": [
        con
    ]
    })
    return(resp)

def get_nft_details(con):
    w3 = common_1()
    resp = w3.provider.make_request('qn_fetchNFTsByCollection', {
    "collection": con,
    "page": 1,
    "perPage": 10
    })
    return(resp)

def nft_transfers(con, token):
    w3 = common_1()
    resp = w3.provider.make_request('qn_getTransfersByNFT', {
    "collection": con,
    "collectionTokenId": str(token),
    "page": 1,
    "perPage": 10
    })
    return(resp)

def nft_owners(wallet, con,token):
    w3 = common_1()
    resp = w3.provider.make_request('qn_verifyNFTsOwner', [wallet, [f"{con}:{token}"]])
    return(resp)

def token_balance(wallet):
    w3 = common_1()
    resp = w3.provider.make_request('qn_getWalletTokenBalance', {
    "wallet": wallet
    })
    return(resp[:5])

def wallet_token_transactions(wallet, con):
    w3 = common_1()
    resp = w3.provider.make_request('qn_getWalletTokenTransactions', {
    "address": wallet,
    "contract": con,
    "page": 1,
    "perPage": 5
    })
    return(resp)

def transactions_by_hash(hash):
    w3 = common_1()
    return(w3.eth.get_transaction(hash))
