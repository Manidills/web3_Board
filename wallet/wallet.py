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
from utils import plt_to_svg, slugify, svg_to_html

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
        # with st.form("form2", clear_on_submit=False): 
        #     wallet_add = st.text_input('Wallet_Address')
        #     area = st.text_input('Enter the place name to generate a LINE MAP image')
        #     submit = st.form_submit_button("Submit")
        # if submit:
        #     token_bal = balance(wallet_add)
        #     est_value = token_bal['balance'].mean()

        #     if est_value > 5:
        #         st.success("Wallet seems not washtraded much, you can generate or mint the FLOWMAP collection NFTS")
        #         st.info(f"{area}")
                # aoi = get_aoi(address=area, distance=500, rectangular=False)
                # df = get_osm_geometries(aoi=aoi)

                # fig = Plot(
                #     df=df,
                #     aoi_bounds=aoi.bounds,
                #     draw_settings=STYLES["Peach"]
                # ).plot_all()
                # st.pyplot(fig)
                # fig.set_size_inches(8, 6)
                # fn = 'scatter.png'
                # fig = io.BytesIO()
                # plt.savefig(fig, format='png',dpi=300, quality=70)
                
                # btn = st.download_button(
                # label="Download image",
                # data=fig,
                # file_name=fn,
                # mime="image/png"
                # )

        import copy

        import numpy as np

        from examples import EXAMPLES
        from utils import (
            image_button_config,
            st_get_osm_geometries,
            st_plot_all,
            get_colors_from_style,
        )
        from prettymapp.geo import GeoCodingError, get_aoi
        from prettymapp.settings import STYLES

        


        if not st.session_state:
            st.session_state.update(EXAMPLES["Macau"])

            lc_class_colors = get_colors_from_style("Peach")
            st.session_state.lc_classes = list(lc_class_colors.keys())
            st.session_state.update(lc_class_colors)
            st.session_state["previous_style"] = "Peach"


        image_button_config()

        example_buttons = [
            column.button(name) for name, column in zip(EXAMPLES.keys(), st.columns(4))
        ]
        selected_example = None
        if any(example_buttons):
            # Set settings for new example
            index_selected = list(np.where(example_buttons))[0][0]
            name_selected = list(EXAMPLES.keys())[index_selected]
            st.session_state.update(EXAMPLES[name_selected].copy())

        st.write("")
        form = st.form(key="form_settings")
        col1, col2, col3 = form.columns([3, 1, 1])

        address = col1.text_input(
            "Location address",
            key="address",
        )
        radius = col2.slider(
            "Radius",
            100,
            1500,
            key="radius",
        )

        style = col3.selectbox(
            "Color theme",
            options=list(STYLES.keys()),
            key="style",
        )

        expander = form.expander("Customize map style")
        col1style, col2style, _, col3style = expander.columns([2, 2, 0.1, 1])

        shape_options = ["circle", "rectangle"]
        shape = col1style.radio(
            "Map Shape",
            options=shape_options,
            key="shape",
        )

        bg_shape_options = ["rectangle", "circle", None]
        bg_shape = col1style.radio(
            "Background Shape",
            options=bg_shape_options,
            key="bg_shape",
        )
        bg_color = col1style.color_picker(
            "Background Color",
            key="bg_color",
        )
        bg_buffer = col1style.slider(
            "Background Size",
            min_value=0,
            max_value=50,
            help="How much the background extends beyond the figure.",
            key="bg_buffer",
        )

        col1style.markdown("---")
        contour_color = col1style.color_picker(
            "Map contour color",
            key="contour_color",
        )
        contour_width = col1style.slider(
            "Map contour width",
            0,
            30,
            help="Thickness of contour line sourrounding the map.",
            key="contour_width",
        )

        name_on = col2style.checkbox(
            "Display title",
            help="If checked, adds the selected address as the title. Can be customized below.",
            key="name_on",
        )
        custom_title = col2style.text_input(
            "Custom title (optional)",
            max_chars=30,
            key="custom_title",
        )
        font_size = col2style.slider(
            "Title font size",
            min_value=1,
            max_value=50,
            key="font_size",
        )
        font_color = col2style.color_picker(
            "Title font color",
            key="font_color",
        )
        text_x = col2style.slider(
            "Title left/right",
            -100,
            100,
            key="text_x",
        )
        text_y = col2style.slider(
            "Title top/bottom",
            -100,
            100,
            key="text_y",
        )
        text_rotation = col2style.slider(
            "Title rotation",
            -90,
            90,
            key="text_rotation",
        )

        if style != "Peach":
            st.session_state.update(get_colors_from_style(style))
        draw_settings = copy.deepcopy(STYLES[style])
        lc_class_colors = get_colors_from_style("Peach")
        for lc_class in list(lc_class_colors.keys()):
            picked_color = col3style.color_picker(lc_class, key=lc_class)
            if "_" in lc_class:
                lc_class, idx = lc_class.split("_")
                draw_settings[lc_class]["cmap"][int(idx)] = picked_color
            else:
                draw_settings[lc_class]["fc"] = picked_color

        form.form_submit_button(label="Submit")

        result_container = st.empty()
        with st.spinner("Creating map... (may take up to a minute)"):
            rectangular = shape != "circle"
            try:
                aoi = get_aoi(address=address, distance=radius, rectangular=rectangular)
            except GeoCodingError as e:
                st.error(f"ERROR: {str(e)}")
                st.stop()
            df = st_get_osm_geometries(aoi=aoi)
            fig = st_plot_all(
                _df=df,
                aoi_bounds=aoi.bounds,
                draw_settings=draw_settings,
                name_on=name_on,
                name=address if custom_title == "" else custom_title,
                font_size=font_size,
                font_color=font_color,
                text_x=text_x,
                text_y=text_y,
                text_rotation=text_rotation,
                shape=shape,
                contour_width=contour_width,
                contour_color=contour_color,
                bg_shape=bg_shape,
                bg_buffer=bg_buffer,
                bg_color=bg_color,
            )

            # result_container.write(html, unsafe_allow_html=True)
            st.pyplot(fig, pad_inches=0, bbox_inches="tight", transparent=True, dpi=300)
        fig.set_size_inches(8, 6)
        svg_string = plt_to_svg(fig)
        html = svg_to_html(svg_string)
        st.write("")
        fname = slugify(address)
        img_format = st.selectbox("Download image as", ["svg", "png", "jpg"], index=0)
        if img_format == "svg":
            data = svg_string
        elif img_format == "png":
            import io
        
            data = io.BytesIO()
            fig.savefig(data, pad_inches=0, bbox_inches="tight", transparent=True)
        st.download_button(label="Download image", data=data, file_name=f"{fname}.{img_format}")

       

        st.session_state["previous_style"] = style

            # else:
            #     st.info("Wallet seems Fishy")
        
    elif op_wallet == "Mint":
        mint_data()
    


        
            



        
        
            
