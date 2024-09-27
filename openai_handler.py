from openai import OpenAI
import pandas as pd
import cryptography_handler

encrypted_val = b'gAAAAABm9fuEW69QQqx9iJj-d7mprLSD_YGeHMmK4MN91z_CwEAJ6YK9dC2v8_9OXfOVx2My8NV-whI0Nff-OG1iJCJcxh8Mvltm4ATeto4Gl8Rvph9JHbRsMEUHsfaFTmmvLXy0WBhwTIwfslvaytSkzk6kOEWNxjh8t4XZZKY3bebAptDnyNn2leK9tZIdRzTV1iiHym987eA-HmvmPx6RUdWrJHuP3W0g8OAgVG5cUJbth2WeAIM0K5IqBFqarvlvDw7RYVDPnPRy2pwq6VaGrzfTXZDQ4mf6wvQ8NHddIfvQbmPHqpE='
key = cryptography_handler.load_key()
open_ai_key = cryptography_handler.decrypt_api_key(encrypted_val, key)

# Function to create the prompt for OpenAI
def create_prompt(table_data, input_text):
    prompt = f"{input_text}:\n"
    for table in table_data:
        prompt += f"\nTable Name: {table['table_name']}\n"
        prompt += f"Columns: {', '.join(table['columns'])}\n"
        prompt += f"Sample Data (2 records): {table['sample_data']}\n"
    return prompt


def open_ai_run_analysis(table_data, input_text):
    prompt = create_prompt(table_data, input_text)
    client = OpenAI(api_key= open_ai_key)
    # Make the API call to OpenAI
    response =  client.chat.completions.with_raw_response.create(
    messages=[
            {"role": "system", "content": "You are a database architect."},
            {"role": "user", "content": prompt}
        ],
    model="gpt-4o-mini").parse()
    return response
    
