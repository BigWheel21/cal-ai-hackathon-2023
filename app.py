import streamlit as st 
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.agents import create_pandas_dataframe_agent
from pandasai import PandasAI
from utils import *
from langchain.chat_models import ChatOpenAI
from pandasai.llm.openai import OpenAI
from PIL import Image

os.environ['OPENAI_API_KEY'] = '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'
chat = get_chatbot(model_name='gpt-4-0613')
openai_api_key = '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'
#data_analyze_agent = create_pandas_dataframe_agent(chat, data, memory=ConversationBufferMemory())
llm = OpenAI(api_token=openai_api_key)
pandas_ai = PandasAI(llm)
fig = None
image = Image.open('/Users/virajbansal/Documents/Logo.png')

st.set_page_config(layout='wide')
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

with col1:
    st.write(' ')

with col2:
    st.write(' ')
    
with col3:
    st.write(' ')
    # st.subheader("Your Co-Pilot in Data Science")

with col4:
    st.title("Code*Char*That      ")

with col5:
    st.write(' ')

with col6:
    st.image(image, width=100)

with col7:
    st.write(' ')

with col8:
    st.write(' ')

with col9:
    st.write(' ')

openai_api_key = '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'
input_csv = st.file_uploader("Upload your CSV file here", type=['csv'])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

code = None

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Done"):
                st.info("Your Query: " + input_text)
                st.session_state.chat_history.append({
                    'user': 'You',
                    'message': input_text
                })


                purpose = detect_qa_or_plot(input_text, chat)
                print(purpose)
                if purpose == 'Plotting':
                    response = generate_visual_code(data, input_text, chat)
                    code = extract_python_code(response)
                    print(code)
                    try:
                        exec(code.replace('fig.show()',''))
                        st.success('AI Response: Ok let me plot for you! Expand below to see the graph!')
                        st.session_state.chat_history.append({
                            'user': 'AI',
                            'message': 'AI Response: Ok let me plot for you! Expand below to see the graph!'
                        })
                    except Exception as e:
                        print(e)
                        st.success("AI Response: Oops! I can't understand, could you elaborate more?")
                        st.session_state.chat_history.append({
                            'user': 'AI',
                            'message': "AI Response: Oops! I can't understand, could you elaborate more?"
                        })
                    
                    
                else:
                    # Run chat_with_csv function
                    #result = get_gpt_response(input_text, chat)
                    result = pandas_ai.run(data, prompt=input_text)
                    st.success("AI Response: "+result)
    if fig is not None:
        for chat in st.session_state.chat_history:
            st.markdown(f"**{chat['user']}:** {chat['message']}")
        
        

        with st.expander('Expand to see the graph'):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.code(code, language='python')
            with col2:
                st.plotly_chart(fig, use_container_width=True)


                