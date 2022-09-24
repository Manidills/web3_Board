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
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/prometheo/aurora-mainnet',
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
                if key_val == 'mints':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('amountUSD', 'id', 'amount0'))
                elif key_val == 'swaps':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('amountUSD', 'id', 'amount0In'))
                elif key_val == 'pairDayDatas':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('dailyVolumeUSD', 'id', 'totalSupply'))
                elif key_val == 'pairs':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('txCount', 'id', 'volumeUSD'))
                elif key_val == 'capitalDexDayDatas':
                    with col2:
                        order_ = st.selectbox(
                        'Order_by',
                        ('dailyVolumeUSD', 'id', 'totalVolumeUSD'))


                submit = st.form_submit_button("Submit")

    if submit:
        payload = {
            "query": query % (val, order_),
        }
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/curioteam/capital-dex-aurora',
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
        res = requests.post(url='https://api.thegraph.com/subgraphs/name/curioteam/capital-dex-aurora',
                            json=payload).json()
        st.write(res)
        download_csv(res)


def aurora_graph():
        auro_main = st.radio('Aurora Explorer', ('Transactions_Explorer', 'Captital_DEX_Aurora'),horizontal=True)

        if auro_main == 'Captital_DEX_Aurora':
            auro_manage = st.radio(
                'Captital_DEX_Aurora',
                ('Capital_DEX_Aurora_Mints','Capital_DEX_Aurora_PairDayDatas','Capital_Dex_Aurora_Token','Capital_Dex_Aurora_Swaps', 'Capital_Dex_Aurora_Swap', 'Capital_Dex_Aurora_Pairs', 'Capital_Dex_Aurora_Day_Datas' ))
            
            if auro_manage == 'Capital_Dex_Aurora_Swaps':
    
                        query = """{ 
                            swaps(first: %s, orderBy: %s, orderDirection: desc) {
                            amount0In
                            amount0Out
                            amount1In
                            amount1Out
                            amountUSD
                            from
                            id
                            logIndex
                            sender
                            timestamp
                            to
                        }
                            }"""
                        multiple_value_dex(query,'swaps')
            elif auro_manage == 'Capital_Dex_Aurora_Swap':
                        query = """{
                                swap(id: \"%s\") {
                                amount0In
                                amount0Out
                                amount1In
                                amount1Out
                                amountUSD
                                from
                                id
                                logIndex
                                sender
                                timestamp
                                to
                            }
                            }"""
                        single_value(query)
                        
            elif auro_manage == 'Capital_DEX_Aurora_Mints':
                        query = """{
                            mints(first: %s, orderBy: %s, orderDirection: desc, subgraphError: allow) {
                                amount0
                                amount1
                                amountUSD
                                feeLiquidity
                                feeTo
                                id
                                liquidity
                                logIndex
                                sender
                                timestamp
                                to
                            }
                            }"""
                        multiple_value_dex(query, 'mints')
            elif auro_manage == 'Capital_DEX_Aurora_PairDayDatas':
                        query = """{
                            pairDayDatas(
                            first: %s
                            orderBy: %s
                            orderDirection: desc
                        ) {
                            dailyTxns
                            dailyVolumeToken0
                            dailyVolumeToken1
                            dailyVolumeUSD
                            date
                            id
                            pairAddress
                            reserve0
                            reserve1
                            reserveUSD
                            totalSupply
                        }
                        }"""
                        multiple_value_dex(query, 'pairDayDatas')
            elif auro_manage == 'Capital_Dex_Aurora_Token':
                        query = """{
                            token(id: \"%s\") {
                            decimals
                            derivedETH
                            id
                            name
                            symbol
                            totalLiquidity
                            totalSupply
                            tradeVolume
                            tradeVolumeUSD
                            txCount
                            untrackedVolumeUSD
                        }
                        }"""
                        single_value(query)
            elif auro_manage == 'Capital_Dex_Aurora_Pairs':
                        query = """{
                            pairs(first: %s, orderBy: %s, orderDirection: desc) {
                            createdAtBlockNumber
                            createdAtTimestamp
                            id
                            liquidityProviderCount
                            reserve0
                            reserveUSD
                            token0Price
                            token1Price
                            totalSupply
                            trackedReserveETH
                            txCount
                            untrackedVolumeUSD
                            volumeToken0
                            volumeToken1
                            volumeUSD
                        }
                        }"""
                        multiple_value_dex(query, 'pairs')
            elif auro_manage == 'Capital_Dex_Aurora_Day_Datas':
                        query = """{
                        capitalDexDayDatas(first: %s, orderBy: %s, orderDirection: desc) {
                            dailyVolumeETH
                            dailyVolumeUSD
                            dailyVolumeUntracked
                            date
                            id
                            totalLiquidityETH
                            totalLiquidityUSD
                            totalVolumeETH
                            totalVolumeUSD
                            txCount
                        }
                        }"""
                        multiple_value_dex(query, 'capitalDexDayDatas')
        
        elif auro_main == 'Transactions_Explorer':
            inp = st.text_input("Enter the address")
            if inp:
                st.subheader("Balance")
                st.write(get_wallet_balance('1313161554', inp))
                st.markdown('#')
                st.subheader("Historical_Portfoilo")
                st.dataframe(get_historical_portfolio('1313161554', inp))
                st.subheader("Transactions")
                st.write(get_transactions('1313161554', inp))

