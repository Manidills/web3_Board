import streamlit as st


import requests

# function to use requests.post to make an API call to the subgraph url
def run_query(query):
    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/ensdomains/ens'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(
            request.status_code, query))


def ens_checker(name):
    # The Graph query - Query ENS name information
    query = """
    {
    domains(where: {name:"%s.eth"}) {
        id
        name
        labelName
        labelhash
    }
    }
    """%(name)
    result = run_query(query)
    if result['data']['domains']:
        return(f"😭 {name}.eth already Found ")
    else:
        return(f'✅ {name}.eth is Available ')
    


def status_check():
    with st.form("form1", clear_on_submit=False): 
                
            val = st.text_input("Enter Domain")
            submit = st.form_submit_button("Submit")
    
    if submit:

        res = ens_checker(name= val)
        st.markdown("#")
        st.info(res) 