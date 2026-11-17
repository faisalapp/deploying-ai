from dotenv import load_dotenv

load_dotenv('.env')
load_dotenv('.secrets')

import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage

from assignment_chat.main import get_graph

graph = get_graph()

def assignment_chat(message: str, history: list[dict]) -> str:
    langchain_messages = []
    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
    langchain_messages.append(HumanMessage(content=message))


    response = graph.invoke({"messages": langchain_messages})

    return response["messages"][-1].content


chat = gr.ChatInterface(fn=assignment_chat)

if __name__ == "__main__":
    chat.launch()