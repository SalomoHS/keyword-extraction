import google.generativeai as genai
import streamlit as st
genai.configure(api_key='AIzaSyBM3MFzxbo_6ptt_o3ss8YchNtjgI7DSRQ')
st.write("Hello world")

model = genai.GenerativeModel(model_name="gemini-1.0-pro")

user_input = st.text_input('Text')
#st.write('The current movie title is', title)

if user_input:
    prompt_parts = [
    f"""{user_input}
    generate 5 keywords from this text""",
    ]


    response = model.generate_content(prompt_parts)
    st.write(response.text)