import io
from statistics import mean
from Apis.covalent import balance, get_historical_portfolio, get_transactions, token_transfers, topic_hash, transaction_hash
from Apis.quicknode import token_balance, token_metadata, wallet_token_transactions
import streamlit as st
from Apis.nftport import  nft_token, nft_trans, wallet_contract_owned, wallet_nft_created, wallet_nft_owned
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
from io import BytesIO
import matplotlib.pyplot as plt

from wallet.mint_image import  mint_data


def wallet():

    op_wallet = st.radio(
    'Wallet Explorer',
    ('NFTS','Tokens','Hash', 'Check_&_Generate_art', 'Mint'),horizontal=True)

    if op_wallet == "NFTS":
        with st.form("form2", clear_on_submit=False): 
            values = ['ethereum', 'polygon']
            window_ANTICOR = st.selectbox('Blockchain_ID', values)
            wallet_add = st.text_input('Wallet_Address')

            submit = st.form_submit_button("Submit")

        if submit:
            st.subheader("NFT Created")
            st.dataframe(wallet_nft_created(window_ANTICOR,wallet_add)['nfts'][:5])
            st.subheader("NFT Owned")
            st.dataframe(wallet_nft_owned(window_ANTICOR,wallet_add)[:2])
            st.subheader("NFT Contract Owned")
            st.dataframe(wallet_contract_owned(window_ANTICOR,wallet_add)[:5])
    elif op_wallet == 'Tokens':
        with st.form("form2", clear_on_submit=False): 
            wallet_add = st.text_input('Wallet_Address')
            contract_add = st.text_input("contract_address")

            submit = st.form_submit_button("Submit")

        if submit:
            st.subheader("Token Balances")
            try:st.write(token_balance(wallet_add))
            except: st.dataframe(balance(wallet_add))
            st.subheader("Historical Portfolio")
            st.dataframe(get_historical_portfolio("1",wallet_add))
            st.subheader("Token Transfers")
            try:st.dataframe(token_transfers(wallet_add,contract_add))
            except: 'NO data'
            st.subheader('Contract_metadata')
            st.write(token_metadata(contract_add)['result'])
            st.subheader("Wallet token transaction")
            st.write(wallet_token_transactions(wallet_add,contract_add))
    elif op_wallet == 'Hash':
        with st.form("form2", clear_on_submit=False): 
            hash = st.text_input('Transaction_Hash or Topic_hash')
            wall = st.text_input("Wallet_address (If topic hash)")

            submit = st.form_submit_button("Submit")

        if submit:
            st.subheader("Transaction Details")
            try:st.dataframe(transaction_hash(hash))
            except:pass
            st.subheader("Topic hash details")
            try:st.dataframe(topic_hash(hash,wall))
            except:pass
    elif op_wallet == 'Check_&_Generate_art':
        with st.form("form2", clear_on_submit=False): 
            wallet_add = st.text_input('Wallet_Address')
            area = st.text_input('Enter the place name to generate a LINE MAP image')
            submit = st.form_submit_button("Submit")
        if submit:
            token_bal = balance(wallet_add)
            est_value = token_bal['balance'].mean()

            if est_value > 5:
                st.success("Wallet seems not washtraded much, you can generate or mint the FLOWMAP collection NFTS")
                st.info(f"{area}")
                aoi = get_aoi(address=area, distance=500, rectangular=False)
                df = get_osm_geometries(aoi=aoi)

                fig = Plot(
                    df=df,
                    aoi_bounds=aoi.bounds,
                    draw_settings=STYLES["Peach"]
                ).plot_all()
                st.pyplot(fig)
                fig.set_size_inches(8, 6)
                fn = 'scatter.png'
                fig = io.BytesIO()
                plt.savefig(fig, format='png',dpi=300, quality=70)
                
                btn = st.download_button(
                label="Download image",
                data=fig,
                file_name=fn,
                mime="image/png"
                )
            else:
                st.info("Wallet seems Fishy")
        
    elif op_wallet == "Mint":
        mint_data()
    


        
            



        
        
            
