import streamlit as st
import pandas as pd
import data_handler
import openai_handler

# Title of the app
st.title("POC - OpenAI Table Analysis")

# Load the CSV from the directory
try:
    # Read the CSV file (we're not displaying the dataframe anymore)
    summary_df = pd.read_csv('summary.csv')
    
    # Input for custom question
    question = st.text_input("Enter your question for OpenAI:", "Give me all the tables that are commercial.")
    
    if st.button("Run Analysis"):
        # Process the data using your data_handler function (not displaying the data)
        table_data = data_handler.return_df_as_table_data(summary_df)
        
        # Run OpenAI analysis with the custom question
        st.write("Running OpenAI analysis...")
        response_data = openai_handler.open_ai_run_analysis(table_data, question)
        
        # Extract the response and display it
        response = response_data.choices[0].message.content
        st.write("OpenAI Response:")
        st.write(response)
except FileNotFoundError:
    st.error("File 'summary.csv' not found in the directory.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
