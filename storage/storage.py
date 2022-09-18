import sqlite3 
from tempfile import NamedTemporaryFile
import ipfsApi
import requests
import streamlit as st
from metamask_component import metamask_component
from pinatapy import PinataPy
from PIL import Image
import pandas as pd

from wallet.ipfs import store_nft_image_ipfs
Image

def create_table():
    connection_obj = sqlite3.connect('ipfs.db')
 
# cursor object
    cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS ipfs")
    
    # Creating table
    table = """ CREATE TABLE ipfs (
                Hash VARCHAR(255) ,
                address STRING(255),
                name STRING(255) 
            ); """
    
    cursor_obj.execute(table)

def upload_pinata(file):
    file = open(file, 'rb')
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

   
    files= {"file": file}
    headers = {
    'Authorization': F'Bearer {"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJiZTJiNjM3ZC04NTRmLTQyYmEtYTFmMC0yNWM5YTAxMWI1ZmQiLCJlbWFpbCI6Im1hbmlkaWxsczQxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI5MGE1MWFhNDEzNGM4NDc1MWIzOCIsInNjb3BlZEtleVNlY3JldCI6IjQ1NGQzYzRmNTA5NGViZTZhNmNkNTVmYTE1NDYxM2RjYWE4ODNjYjBlNWQ1MWU0MTQ4NjcyMDIwZWM5NGFkZjgiLCJpYXQiOjE2NjM1MDY5Nzl9.wO-n4WOJqfpt2kGXdVAbhOkH6uq8Kaw9d7wK8XL9Xhk"}'
    }

    response = requests.request("POST", url, headers=headers, files=files)

    return(response.json())

def storage():
    op_store = st.radio(
    'Storage',
    ('Upload','Check'),horizontal=True)
    value = metamask_component(account_results="hello there")
    if op_store == "Upload":
       
        if value:
            st.write(value)

            st.subheader("Upload FLOWMAP IMAGE ")
            with st.form("form2", clear_on_submit=False): 
                image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
                name = st.text_input("Enter file name")
                submit = st.form_submit_button("Submit")
            if submit:
                temp_file = NamedTemporaryFile(delete=False)
                temp_file.write(image_file.getvalue())
                api = store_nft_image_ipfs(temp_file.name)
                st.subheader("IPFS_Upload_Details")
                st.write(api)
                connection_obj = sqlite3.connect('ipfs.db')
                cursor_obj = connection_obj.cursor()
                cursor_obj.execute("INSERT INTO ipfs values(?, ?, ?)", (str(api['ipfs_url']), str(value), str(name)))
                data=cursor_obj.execute('''SELECT * FROM ipfs''')
                for row in data:
                    print(row)

                # Commit your changes in the database    
                connection_obj.commit()

                # Closing the connection
                connection_obj.close()
                st.info("Data Inserted")
    elif op_store == "Check":
        if value:
            cnx = sqlite3.connect('ipfs.db')
            df = pd.read_sql_query(f"SELECT * FROM ipfs", cnx)
            st.dataframe(df)
    


