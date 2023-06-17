from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def get_chatbot(model_name='gpt-4-0613'):
    chat = ChatOpenAI(model_name=model_name)
    return chat

def generate_visual_code(data, prompt, chat):

    sys_msg = SystemMessage(content = 
    f"""
    You are a Python programmer who uses Plotly package to visualize data. You have the following data in the python pandas format: {data}. 
    You will write plot functions like:
    import plotly
        ...
    fig = ...
    """)

    prompt_template = f"""
    {prompt} Generate the python code for this plot using Plotly package. 
    """ 
    human_msg = HumanMessage(content = prompt_template)
    res = chat([sys_msg, human_msg])
    return res

def extract_python_code(text):
    index1 = text.find('```python\n')
    index2 = text[index1:].find('\n```')
    code = text[index1+len('```python\n'):index1+index2]
    return code


