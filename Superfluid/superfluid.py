from Superfluid.super_arbi import superfluid_arbi
from Superfluid.super_avax import superfluid_avax
from Superfluid.super_dash import super_charts
from Superfluid.super_matic import superfluid_matic
from Superfluid.super_opti import superfluid_opti
from Superfluid.super_xdai import superfluid_xdai
import streamlit as st

def super_graph():
        super_main = st.radio('Superfluid Explorer', ('Superfluid_streams', 'Superfluid_xdai', 'Superfluid_matic', 'Superfluid_Avalanche','Superfluid_Optimism', 'Superfluid_Arbitrum'),horizontal=True)

        if super_main == 'Superfluid_streams':
            super_charts()
        elif super_main == 'Superfluid_xdai':
            superfluid_xdai()
        elif super_main == 'Superfluid_matic':
            superfluid_matic()
        elif super_main == 'Superfluid_Avalanche':
            superfluid_avax()
        elif super_main == 'Superfluid_Optimism':
            superfluid_opti()
        elif super_main == 'Superfluid_Arbitrum':
            superfluid_arbi()