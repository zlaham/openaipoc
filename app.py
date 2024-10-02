import streamlit as st
import pandas as pd
import data_handler
import openai_handler
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Title of the app
st.title("POC - OpenAI Table Analysis")
logger.info("App started")

# Load the CSV from the directory
try:
    logger.info("Attempting to read 'summary.csv'")
    summary_df = pd.read_csv('summary.csv')
    logger.info("CSV file loaded successfully")
    
    # Input for custom question
    question = st.text_input("Enter your question for OpenAI:", "Give me all the tables that are commercial.")
    
    if st.button("Run Analysis"):
        logger.info("Analysis button clicked with question: %s", question)

        # Process the data using your data_handler function
        logger.info("Processing data with data_handler")
        table_data = data_handler.return_df_as_table_data(summary_df)
        logger.info("Data processing complete")
        
        # Run OpenAI analysis with the custom question
        st.write("Running OpenAI analysis...")
        logger.info("Sending data to OpenAI")
        response_data = openai_handler.open_ai_run_analysis(table_data, question)
        logger.info("Received response from OpenAI")

        # Extract the response and display it
        response = response_data.choices[0].message.content
        st.write("OpenAI Response:")
        st.write(response)
        logger.info("OpenAI response displayed successfully")
except FileNotFoundError as fnf_error:
    st.error("File 'summary.csv' not found in the directory.")
    logger.error("FileNotFoundError: %s", str(fnf_error))
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logger.error("Exception occurred: %s", str(e))
