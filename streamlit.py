import streamlit as st
import pandas as pd
from datetime import datetime
import requests

def run(model, inputs):
        input = { "messages": inputs , 'raw':'true'}
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
        return response.json()

if 'summary_list' not in st.session_state:
    st.session_state['summary_list'] = []
if 'state' not in st.session_state:
    st.session_state['state'] = 0
    
uploaded_file = st.file_uploader("Upload Excel file")
    
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/6a4d9b68ee082caad2a5a9260dbd6c38/ai/run/"
    headers = {"Authorization": "Bearer 5pnUivTXlD-6qAdQT0v_sNYRmFMgH7EaGxjVgt2D"}

    while(1):
        for i,row in df.iloc[st.session_state['state']:].iterrows():
            inputs = [
                { "role": "system", "content": "You are an assistant that helps to summarize news" },
                { "role": "user", "content": f"Summarize following news into 3 sentences: {row['translated']}"}
            ]
            output = run("@cf/mistral/mistral-7b-instruct-v0.2-lora", inputs)
            st.session_state['summary_list'].append(output["result"]["response"])
            
            st.session_state['state']+=1

        if len(st.session_state['summary_list']) == len(df):
            break
        
    df['summarized'] = st.session_state['summary_list']
    
    final_df = df.copy()
    file_name = f"{datetime.now().strftime('%Y%m%d')}_news_summarized.csv"
    excel_file = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data",
        data=excel_file,
        file_name=file_name
    )
