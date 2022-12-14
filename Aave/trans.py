from datetime import datetime, timezone
from enum import Enum
import pandas as pd
import pytz
import requests
import streamlit as st




def trans():

    class Chain(Enum):
        Ethereum = 'Ethereum'
        Optimism = 'Optimism'
        Arbitrum = 'Arbitrum'
        Polygon_v3 = 'Polygon v3'
        Polygon_V2 = 'Polygon v2'
        Avalanche_v2 = 'Avalanche v2'
        Avalanche_v3 = 'Avalanche v3'
        Harmony = 'Harmony'
        Fantom = 'Fantom'

    def get_chain_info(chain_name: Chain):
        if chain_name == Chain.Avalanche_v2:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v2-avalanche-extended',
                    'https://snowtrace.io/address/',
                    'https://snowtrace.io/tx/'
                    ]
        if chain_name == Chain.Avalanche_v3:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-avalanche',
                    'https://snowtrace.io/address/',
                    'https://snowtrace.io/tx/'
                    ]
        if chain_name == Chain.Ethereum:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v2-ethereum-extended',
                    'https://etherscan.io/address/',
                    'https://etherscan.io/tx/'
                    ]
        if chain_name == Chain.Optimism:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-optimism-extended',
                    'https://optimistic.etherscan.io/address/',
                    'https://optimistic.etherscan.io/tx/'
                    ]
        if chain_name == Chain.Polygon_v3:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-polygon-extended',
                    'https://polygonscan.com/address/',
                    'https://polygonscan.com/tx/'
                    ]
        if chain_name == Chain.Polygon_V2:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v2-polygon-extended',
                    'https://polygonscan.com/address/',
                    'https://polygonscan.com/tx/'
                    ]
        if chain_name == Chain.Harmony:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-harmony-extended',
                    'https://explorer.harmony.one/address/',
                    'https://explorer.harmony.one/tx/'
                    ]
        if chain_name == Chain.Fantom:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-fantom-extended',
                    'https://ftmscan.com/address/',
                    'https://ftmscan.com/tx/'
                    ]
        if chain_name == Chain.Arbitrum:
            return ['https://api.thegraph.com/subgraphs/name/messari/aave-v3-arbitrum-extended',
                    'https://arbiscan.io/address/',
                    'https://arbiscan.io/tx/'
                    ]


    def humanized_time(ts_start):
        ts_end = datetime.utcnow().replace(tzinfo=timezone.utc)
        ts_diff = ts_end - ts_start
        secs = ts_diff.total_seconds()
        days, secs = divmod(secs, secs_per_day := 60 * 60 * 24)
        hrs, secs = divmod(secs, secs_per_hr := 60 * 60)
        mins, secs = divmod(secs, secs_per_min := 60)
        answer2 = ''
        if days != 0:
            answer2 += f'{int(days)} days '
        if hrs != 0:
            answer2 += f'{int(hrs)} hrs '

        if mins != 0:
            answer2 += f'{int(mins)} mins '
        else:
            answer2 += f'{int(secs)} secs '
        return answer2 + ' ago'


    def fetch_data(chain: Chain, tr_hash):
        payload = {
            "query": """{ 
            withdraws(first: 10, where: { hash: \"%s\" }){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
            deposits(first: 10, where: { hash: \"%s\" }){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
            borrows(first: 10, where: { hash: \"%s\" }){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
            repays(first: 10, where: { hash: \"%s\" }){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
            liquidates(first: 10, where: { hash: \"%s\" }){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} } }""" % (
                tr_hash, tr_hash, tr_hash, tr_hash, tr_hash),
        }
        res = requests.post(url=get_chain_info(chain)[0],
                            json=payload).json()['data']
        if res:
            actions = clean_data(res, chain)
        else:
            return False

        return actions


    def get_type_name(item: str):
        return item[:-1].capitalize()


    def get_explorer_user_address(user_address: str, chain):
        return str(get_chain_info(chain)[1] + user_address)


    def get_explorer_transaction_address(transaction_address: str, chain):
        return get_chain_info(chain)[2] + transaction_address


    def clean_data(res, chain):
        actions = []
        for item in ['withdraws', 'deposits', 'borrows', 'repays', ]:
            if not res[item]:
                continue
            action_content_list = res[item]
            for action in action_content_list:
                clean_action = {}
                clean_action['Time'] = datetime.fromtimestamp(int(action['timestamp']), ).strftime(
                    "%m/%d/%Y, %H:%M:%S")
                clean_action['py_date'] = datetime.fromtimestamp(int(action['timestamp']), pytz.timezone("UTC"))
                clean_action['Type'] = get_type_name(item)
                clean_action['Asset Symbol'] = action['asset']['symbol']
                clean_action['transaction_hash'] = action['hash']
                clean_action['Asset ID'] = action['asset']['id']
                clean_action['Asset Amount'] = float(int(action['amount']) / pow(10, int(action['asset']['decimals'])))
                clean_action['Amount USD'] = action['amountUSD']
                clean_action['user'] = action['account']['id']
                clean_action['logIndex'] = action['logIndex']
                clean_action['chain'] = chain.value
                actions.append(clean_action)
        return actions


    
    c1, c2, c3 = st.columns((1, 2, 1))

    input_hash = c2.text_input('Enter Transaction Hash:',
                            '0x0784ff9cf55478cc6b389b0028f9d4da9556a8ca36b4ccbce4f21b2ecf756e72',
                            placeholder='Input the Transaction Hash')

    data = ''
    selected_chain = ''
    for chain_item in Chain:
        data = fetch_data(chain_item, input_hash)
        # find the right data so exit and don't search in next chains
        if data:
            selected_chain = chain_item
            break
    if not data:
        st.warning('Hash Address is not valid!')
    else:
        df = pd.DataFrame(
            data,
            columns=["Time", "Type", "Asset Symbol", "Asset Amount", "Amount USD", "Asset ID", "user",
                    "logIndex"]).sort_values('logIndex')
        st.markdown('---')

        c1, c2 = st.columns(2)
        c1.markdown('#### Transaction Hash: ')
        c1.markdown(
            f"<a style='text-decoration: none;' href='{get_explorer_transaction_address(data[0]['transaction_hash'], selected_chain)}'>{data[0]['transaction_hash']}</a>",
            unsafe_allow_html=True)
        c2.markdown(
            f'<span style="font-family:sans-serif; color:grey; font-size: 18px;">Timestamp (UTC): </span><span style="font-family:sans-serif; color:purple; font-size: 16px;">{humanized_time(data[0]["py_date"])}</span>',
            unsafe_allow_html=True)
        c2.markdown(
            f'<span style="font-family:sans-serif; color:grey; font-size: 22px;">Chain: </span><span style="font-family:sans-serif; color:purple; font-size: 20px;">{selected_chain.value}</span>',
            unsafe_allow_html=True)
        st.markdown('#### Actions: ')
        st.table(df)


    # lastest transactions
    def create_latest():
        def fetch_latest_transactions(chain: Chain):
            payload = {
                "query": """{ 
                withdraws(first: 10, orderBy: blockNumber, orderDirection: desc, where:{timestamp_gte: 1659815794}){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } }
                    deposits(first: 10, orderBy: blockNumber, orderDirection: desc, where:{timestamp_gte: 1659815794}){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
                    borrows(first: 10, orderBy: blockNumber, orderDirection: desc, where:{timestamp_gte: 1659815794}){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } } 
                    repays(first: 10, orderBy: blockNumber, orderDirection: desc, where:{timestamp_gte: 1659815794}){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} account { id } }
                    liquidates(first: 10, orderBy: blockNumber, orderDirection: desc, where:{timestamp_gte: 1659815794}){ id hash logIndex timestamp amount amountUSD asset {symbol decimals id} } }""",
            }
            res = requests.post(url=get_chain_info(chain)[0],
                                json=payload).json()['data']
            if res:
                actions = clean_data(res, chain)
            else:
                return False

            return actions

        latest_data = []
        for chain_item in Chain:
            latest_data.extend(fetch_latest_transactions(chain_item))
        if not latest_data:
            st.warning('Error!')
        else:
            latest_df = pd.DataFrame(
                latest_data,
                columns=["Time", "transaction_hash", "Type", "Asset Symbol", "Asset Amount", "Amount USD", "chain",
                        "logIndex"])

            latest_df = latest_df.sort_values('Time', ascending=False)
            return latest_df


    st.write('')
    st.write('')
    st.title('lastest transactions')

    if 'latest_df' not in st.session_state:
        latest_df = create_latest()
        st.session_state.latest_df = latest_df
    st.table(st.session_state.latest_df.head(20))

    # end latest
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
