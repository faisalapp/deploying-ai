import os
from dotenv import load_dotenv



load_dotenv(".env")
load_dotenv(".secrets")

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from assignment_chat.prompts import return_instructions
from assignment_chat.tools_weather import get_current_weather
from assignment_chat.tools_search import search_documents
from assignment_chat.tools_service3 import convert_units

chat_agent = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.7,
    base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1',
    api_key='any value',
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)

tools = [get_current_weather, search_documents, convert_units]

def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = chat_agent.bind_tools(tools).invoke(
        [SystemMessage(content=return_instructions())] + state["messages"]
    )
    return {"messages": [response]}

def get_graph():
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))            # 1
    builder.add_edge(START, "call_model")        # 2
    builder.add_conditional_edges(               # 3
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")      # 4
    return builder.compile()

if __name__ == "__main__":
    from langchain_core.messages import HumanMessage
    graph = get_graph()
    #result = graph.invoke({"messages": [HumanMessage(content="What's the weather in Toronto right now?")]})    
    #result = graph.invoke({"messages": [HumanMessage(content="According to the report, why do so many enterprise AI pilots fail to scale?")]})
    result = graph.invoke({"messages": [HumanMessage(content="Marlowe, it's 30 degrees Celsius here — what's that in Fahrenheit?")]})
    print(result["messages"][-1].content)