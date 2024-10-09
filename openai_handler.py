#from openai import OpenAI
import pandas as pd
import cryptography_handler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import getpass
import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

encrypted_val = b'gAAAAABm9fuEW69QQqx9iJj-d7mprLSD_YGeHMmK4MN91z_CwEAJ6YK9dC2v8_9OXfOVx2My8NV-whI0Nff-OG1iJCJcxh8Mvltm4ATeto4Gl8Rvph9JHbRsMEUHsfaFTmmvLXy0WBhwTIwfslvaytSkzk6kOEWNxjh8t4XZZKY3bebAptDnyNn2leK9tZIdRzTV1iiHym987eA-HmvmPx6RUdWrJHuP3W0g8OAgVG5cUJbth2WeAIM0K5IqBFqarvlvDw7RYVDPnPRy2pwq6VaGrzfTXZDQ4mf6wvQ8NHddIfvQbmPHqpE='
key = cryptography_handler.load_key()
open_ai_key = cryptography_handler.decrypt_api_key(encrypted_val, key)

os.environ["OPENAI_API_KEY"] = open_ai_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()

model = ChatOpenAI(model="gpt-4o-mini")

# Function to create the prompt for OpenAI
def create_prompt(table_data, input_text):
    prompt = f"{input_text}:\n"
    for table in table_data:
        prompt += f"\nTable Name: {table['table_name']}\n"
        prompt += f"Columns: {', '.join(table['columns'])}\n"
        prompt += f"Sample Data (2 records): {table['sample_data']}\n"
    return prompt

# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)
# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)
# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

def open_ai_run_analysis(table_data, input_text, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    prompt = create_prompt(table_data, input_text)
    messages = [
        SystemMessage(content="You are a database architect"),
        HumanMessage(content=prompt),
    ]
    output = app.invoke({"messages": messages}, config)
    save_content(input_text, output["messages"][-1].content,thread_id)
    return output["messages"][-1].content

def save_content(question, answer, thread_id):
    with open(thread_id+"_data.json", "a") as file:
            file.write(question+"\n")
            file.write(answer+"\n")


# def save_content(thread_id, Q_A):
#     with open(thread_id+"_data.json", "w") as file:
#         for index, line in enumerate(Q_A["messages"]):
#             if index > 0:
#                 statment = line.content
#                 if isinstance(line, HumanMessage):
#                     statment = substring_until_keyword(line.content, "\n\nTable Name")
#                 file.write(statment)
#                 file.write("================================")

# def substring_until_keyword(sentence, keyword):
#     index = sentence.find(keyword)
#     if index != -1:
#         return sentence[:index]
#     else:
#         return sentence  # Return the whole string if the keyword is not found

