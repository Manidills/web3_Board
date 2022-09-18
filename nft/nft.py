from statistics import mean, median
from Apis.nftport import contract_stats, dupliacte, nft_token, nft_trans
from Apis.quicknode import  get_nft_details, nft_contract_metadata, nft_transfers, token_metadata
from nft.rarity import rarity
import streamlit as st



def token_extract():
    with st.form("form1", clear_on_submit=False): 
        values = ['ethereum', 'polygon']
        window_ANTICOR = st.selectbox('Blockchain_ID', values)
        title = st.text_input('Contract_address')
        token_add = st.text_input('Token_ID')

        submit = st.form_submit_button("Submit")

    if submit:
        col1, col2 = st.columns((2,2))
        with col1:
            try:
                metadata = nft_contract_metadata(title)
                if metadata['result']:
                    st.subheader("Collection_Metadata")
                    st.write(metadata)
                else:
                    st.subheader("Collection_Stats")
                    st.write(contract_stats(window_ANTICOR,title))
            except:
                st.subheader("Collection_Stats")
                st.write(contract_stats(window_ANTICOR,title))
        with col2:
            st.subheader("Token")
            nft_data = nft_token(window_ANTICOR,title,token_add)
            try:st.image(nft_data['nft']['metadata']['image_url'], width = 400)
            except:pass
            st.write(nft_data['contract'])
        
        st.subheader("NFT_Transactions")
        try:st.dataframe(nft_transfers(title,token_add)['result']['transfers'])
        except: st.dataframe(nft_trans(window_ANTICOR,title,token_add))

        nft_tran = nft_trans(window_ANTICOR,title,token_add)
        if nft_tran is None:
            pass
        
        else:
            try:
                est_value = mean([d.get('price_usd') for d in nft_tran.price_details])
                sum_value = sum([d.get('price_usd') for d in nft_tran.price_details])
                min_value = min([d.get('price_usd') for d in nft_tran.price_details])
                max_value = max([d.get('price_usd') for d in nft_tran.price_details])
                median_value = median([d.get('price_usd') for d in nft_tran.price_details])
            
                st.success(f"Estimated Value To Buy This NFT :${est_value}")
                st.write(f"Total_Sum: ${sum_value}")
                st.write(f"Min_value: ${min_value}")
                st.write(f"Max_value: ${max_value}")
                st.write(f"Median_value: ${median_value}")
                st.markdown("#")
                st.subheader("Token Transactions")
            except:
                st.info('Not much details to analyze')
            st.subheader('Activity_Details')
            try:st.dataframe(nft_tran)
            except:pass

        dups=dupliacte(window_ANTICOR,title,token_add)['similar_nfts']
        st.subheader("Similar NFTS")
        st.table(dups)
    else:
        rarity()
        
        