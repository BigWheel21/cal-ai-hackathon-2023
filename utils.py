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
    assume that the data has been loaded by Pandas package with the variable name "data".
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
    return res.content

def extract_python_code(text):
    index1 = text.find('```python\n')
    index2 = text[index1:].find('\n```')
    code = text[index1+len('```python\n'):index1+index2]
    return code

def get_gpt_response(prompt, chat):
    human_msg = HumanMessage(content = prompt)
    response = chat([human_msg])
    return response.content

def detect_qa_or_plot(prompt, chat):
    
    prompt_template = """
        The following kinds of questions are related to Plotting:
        - Create a line plot for ...
        - Plot ....
        - Generate a graph ...
        
        The following kinds of questions are related to Q&A:
        - Do an analysis for ...
        - How is ....
        - Why the stocks are going down?
        
        """+f"""
    '{prompt}'
    Is this a task for "Plotting" or "Q&A".
    Reply in the format:
    category: 
    """
    human_msg = HumanMessage(content = prompt_template)
    res = chat([human_msg])
    return res.content.split(' ')[-1]