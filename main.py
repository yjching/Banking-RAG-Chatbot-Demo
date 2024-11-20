import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

import streamlit as st
import requests
import json
import io

st.image("commonwealth-bank-logo-png-icon-diamond-300x300.png",width=100)
st.title("CBA Bank Chat Application")

st.markdown("Welcome to CBA Bank Chat - where you can chat with assistant and get all of your questions answered. Please note our assistant is only here to help on CBA related questions and topics. ")

url = "https://apgtps2demo.gtp.unx.sas.com"
auth_url = f"{url}/SASLogon/oauth/token"
## reading long-lived refresh token from txt file
refresh_token = os.getenv("SAS_VIYA_REFRESH_TOKEN")
payload=f'grant_type=refresh_token&refresh_token={refresh_token}'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic c2FzLmNsaTo=',
}
response = requests.request("POST", auth_url, headers=headers, data=payload, verify=False)
access_token = response.json()['access_token']

def call_rag_api(input):
    print(input)
    input_user_prompt = input[-1]
    print(input_user_prompt)
    url = "https://apgtps2demo.gtp.unx.sas.com/microanalyticScore/modules/rag_chatbot_guardrail/steps/execute"

    payload = json.dumps({
    "version": 1,
    "inputs": [
        {"name": "content_", "value": f"{input_user_prompt}"},
        {"name": "__uniqueid___","value": 1}
    ]
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.json())

    output_json = response.json()['outputs']

    for output in output_json:
        if output['name'] == "Final_Response":
            guardrail_output = output['value']
        if output['name'] == "answer_llm":
            text_output = output['value']
    
    if text_output is None:
        app_response = guardrail_output
    elif guardrail_output is None:
        app_response = text_output
    return app_response

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        stream = call_rag_api([
                m["content"]
                for m in st.session_state.messages
            ])
        response = st.write_stream(io.StringIO(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})
