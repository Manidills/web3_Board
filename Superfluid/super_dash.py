from common.connect import *
import streamlit as st


def super_charts():
    
    st.markdown('#')

    data = connect('db/superfluid.db')
    st.markdown("#")
    st.title("Super_Fluid")

    line_chart_multi(data, 'superfluid_Total_Flow_Testing', 'day', 'active_streams', 'symbol','superfluid_active_streams')
    line_chart_multi(data, 'superfluid_Total_Flow_Testing', 'day', 'flow_per_stream', 'symbol','superfluid_flow_per_stream')
    line_chart_multi(data, 'superfluid_Total_Flow_Testing', 'day', 'all_sum_flowrate', 'symbol','superfluid_all_sum_flowrate')

    st.subheader("Superfluid_CFA_Active_Streams_by_User_Polygon")
    st.dataframe(table(data, 'Superfluid_CFA_Active_Streams_by_User_Polygon'))

    st.subheader("superfluid_Recent_active_streamers")
    st.dataframe(table(data, 'superfluid_Recent_active_streamers'))

    st.subheader("Superfluid_Share_of_Streams_by_Age_Polygon")
    st.dataframe(table(data, 'Superfluid_Share_of_Streams_by_Age_Polygon'))

    

    
