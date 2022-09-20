import imp
from Aave.aave_optimisim import aave_opti
from Aave.aave_polygon import aave_poly
from Aave.app import trans_explore
from Aave.trans import trans
import streamlit as st
from PIL import Image

def aave_v3():
    
    
    options_polygon = st.radio(
    'Explorer',
    ('Transactions_Explorer','Repay_Deposit_Borrow_Explorer','Polygon','Optimisim',),horizontal=True)

    st.markdown("#")
    st.title("Aave v3 Explorer")
    st.image(Image.open("Aave/aave.png"))
    
    if options_polygon == 'Polygon':
        aave_poly()
    elif options_polygon == 'Optimisim':
        aave_opti()
    elif options_polygon == 'Transactions_Explorer':
        trans()
    elif options_polygon == 'Repay_Deposit_Borrow_Explorer':
        trans_explore()