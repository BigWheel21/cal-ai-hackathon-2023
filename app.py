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

os.environ['OPENAI_API_KEY'] = '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'
chat = get_chatbot(model_name='gpt-4-0613')
openai_api_key = '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'
#data_analyze_agent = create_pandas_dataframe_agent(chat, data, memory=ConversationBufferMemory())
llm = OpenAI(api_token=openai_api_key)
pandas_ai = PandasAI(llm)
fig = None

st.set_page_config(layout='wide')
st.title("AI Visualizer - AI Data Visualization and Analysis")

openai_api_key = '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'
input_csv = st.file_uploader("Upload your CSV file here", type=['csv'])

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
                
                purpose = detect_qa_or_plot(input_text, chat)
                
                if purpose == 'Plotting':
                    response = generate_visual_code(data, input_text, chat)
                    code = extract_python_code(response)
                    print(code)
                    try:
                        exec(code.replace('fig.show()',''))
                        st.success('AI Response: Ok let me plot for you! Expand below to see the graph!')
                    except:
                        st.success("AI Response: Oops! I can't understand, could you elaborate more?")

                else:
                    # Run chat_with_csv function
                    #result = get_gpt_response(input_text, chat)
                    result = pandas_ai.run(data, prompt=input_text)
                    st.success("AI Response: "+result)
    if fig is not None:
        with st.expander('Expand to see the graph'):
            st.plotly_chart(fig, use_container_width=True)


                