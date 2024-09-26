from openai import OpenAI
import pandas as pd

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
    client = OpenAI(api_key= "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")
    # Make the API call to OpenAI
    response =  client.chat.completions.with_raw_response.create(
    messages=[
            {"role": "system", "content": "You are a database architect."},
            {"role": "user", "content": prompt}
        ],
    model="gpt-4o-mini").parse()
    return response
    
