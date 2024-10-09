import streamlit as st
import pandas as pd
import data_handler
import openai_handler
import logging
import uuid
import os

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

# Function to load and cache the CSV
@st.cache_data
def load_csv():
    logger.info("Loading CSV file")
    return pd.read_csv('summary.csv')

# Title of the app
st.title("POC - OpenAI Table Analysis")
logger.info("App started")
def check_first_load():
    if 'first_load' not in st.session_state:
        st.session_state.first_load = True
        st.session_state.thread_id = uuid.uuid1().hex
        st.session_state.file_content = ""
    else:
        st.session_state.first_load = False

# Call the function
check_first_load()
logger.error(st.session_state.first_load)

try:
    # Display status
    #if st.session_state.first_load:
    #    thread_id = uuid.uuid1().hex
    if os.path.exists(st.session_state.thread_id+'_data.json'):
        with open(st.session_state.thread_id+'_data.json', 'r') as file:
            st.session_state.file_content = file.read()
    if st.session_state.file_content!="":             
        button_clicked = st.download_button(label="Download File", data=st.session_state.file_content, file_name="data.txt")#, # Name of the file to download mime="text/plain" # MIME type for plain text ):
        if button_clicked:
            st.session_state.first_load = True
            st.session_state.thread_id = uuid.uuid1().hex
            st.session_state.file_content = ""
except Exception as e:
    logger.error("Exception occurred: %s", str(e))

try:
    # Load the CSV using caching
    summary_df = load_csv()
    logger.info("CSV file loaded successfully (from cache if applicable)")
    
    # Input for custom question
    question = st.text_input("Enter your question for OpenAI:", "Give me all the tables that are commercial.")

    if st.button("Run Analysis"):
        logger.info("Analysis button clicked with question: %s", question)

        # Process the data using your data_handler function
        logger.info("Processing data with data_handler")
        table_data = data_handler.return_df_as_table_data(summary_df)
        logger.info("Data processed successfully, table data prepared")

        # Log the data being sent to OpenAI (sanitized if necessary)
        logger.info("Sending the following data to OpenAI: %s", str(table_data))

        # Run OpenAI analysis with the custom question
        st.write("Running OpenAI analysis...")
        
        try:
            logger.info("Sending data to OpenAI with question: %s", question)
            response_data = openai_handler.open_ai_run_analysis(table_data, question, st.session_state.thread_id)
            logger.info("OpenAI response received")

            # Extract the response and display it
            response = response_data#.choices[0].message.content
            st.write("OpenAI Response:")
            st.write(response)
            logger.info("OpenAI response displayed successfully")
        # except openai.error.OpenAIError as api_error:
        #     st.error("An OpenAI error occurred: " + str(api_error))
        #     logger.error("OpenAIError: %s", str(api_error))
        except Exception as e:
            st.error(f"An error occurred while communicating with OpenAI: {str(e)}")
            logger.error("Exception during OpenAI call: %s", str(e))
except FileNotFoundError as fnf_error:
    st.error("File 'summary.csv' not found in the directory.")
    logger.error("FileNotFoundError: %s", str(fnf_error))
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logger.error("Exception occurred: %s", str(e))
