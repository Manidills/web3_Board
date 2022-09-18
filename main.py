from Aave.aave import aave_v3
from Aurora.aurora import aurora_graph
from Ens.ens import ens
from Superfluid.superfluid import super_graph
from Yearn.yearn import yearn
from nft.nft import token_extract
from skale.skale import skl
from storage.storage import storage
import streamlit as st
from streamlit_option_menu import option_menu
from wallet.wallet import wallet


st.set_page_config(
    page_title="Web3 Board",
    layout="wide"
)

col1, col2, col3 = st.columns([1,1.5,1])

with col1:
    st.write(' ')

with col2:
    new_title = '<p style="font-family: Tangerine; text-align: center; color:white; font-size: 70px;">Web3 Board</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    

with col3:
    st.write(' ')


st.markdown("#")
option = option_menu("Web3 Board", ['Web3','NFT_Token', 'Wallet','Storage'], 
    icons=['house'], menu_icon="cast", default_index=0, orientation="horizontal")

if option == 'Web3':
    
    st.markdown('#')
    
    option_web3 = st.selectbox('SELECT WEB3 PROTOCOL',('Aave','Yearn','Skale','Ens', 'Aurora', 'Superfluid'))
    st.markdown("#")

   
    if option_web3 == 'Aave':
        aave_v3()
    elif option_web3 == 'Yearn':
        yearn()
    elif option_web3 == 'Skale':
        skl()
    elif option_web3 == 'Ens':
        ens()
    elif option_web3 == 'Aurora':
        aurora_graph()
    elif option_web3 == 'Superfluid':
        super_graph()

elif option == 'NFT_Token':
    token_extract()

elif option == 'Wallet':
    wallet()

elif option == 'Storage':
    storage()