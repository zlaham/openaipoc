import streamlit as st
import pandas as pd
import data_handler
import openai_handler
import logging
import uuid
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import cryptography_handler

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
        st.session_state.page = "run_analysis"  # Initialize page state
    else:
        st.session_state.first_load = False

# Call the function
check_first_load()

download_button_disabled = False

# Page for "Run Analysis"
def run_analysis_page():
    try:
        # Load the CSV using caching
        summary_df = load_csv()
        logger.info("CSV file loaded successfully (from cache if applicable)")
        
        # Input for custom question
        question = st.text_input("Enter your question for OpenAI:", "Give me all the tables that are commercial.")

        if st.button("Run Analysis"):
            st.session_state.first_load = False
            logger.info("Analysis button clicked with question: %s", question)

            # Process the data using your data_handler function
            logger.info("Processing data with data_handler")
            table_data = data_handler.return_df_as_table_data(summary_df)
            logger.info("Data processed successfully, table data prepared")

            st.write("Running OpenAI analysis...")

            try:
                logger.info("Sending data to OpenAI with question: %s", question)
                response_data = openai_handler.open_ai_run_analysis(table_data, question, st.session_state.thread_id)
                logger.info("OpenAI response received")

                response = response_data
                st.write("OpenAI Response:")
                st.write(response)
                logger.info("OpenAI response displayed successfully")

            except Exception as e:
                st.error(f"An error occurred while communicating with OpenAI: {str(e)}")
                logger.error("Exception during OpenAI call: %s", str(e))

    except FileNotFoundError as fnf_error:
        st.error("File 'summary.csv' not found in the directory.")
        logger.error("FileNotFoundError: %s", str(fnf_error))
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error("Exception occurred: %s", str(e))

# Page for "Dataset Analysis"
def dataset_analysis_page():
    st.write("Dataset Analysis Page")

    # List of S3 paths
    s3_paths = [
        's3://processed.lenora.dataset/syhdr_commercial_inpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_commercial_outpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_commercial_person_2016.csv',
        's3://processed.lenora.dataset/syhdr_commercial_pharmacy_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicaid_inpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicaid_outpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicaid_person_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicaid_pharmacy_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicaid_provider_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicare_inpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicare_outpatient_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicare_person_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicare_pharmacy_2016.csv',
        's3://processed.lenora.dataset/syhdr_medicare_provider_2016.csv'
    ]
    
    # Create a combobox (selectbox)
    selected_file = st.selectbox("Select a dataset:", s3_paths)

    # Store the selected dataset and loaded DataFrame in session state
    if st.button("Load Dataset"):
        st.write(f"Loading dataset: {selected_file}")
        try:
            pandas_df = data_handler.return_pandas_df_from_csv(selected_file)
            st.session_state['pandas_df'] = pandas_df  # Store DataFrame in session state

            st.write(pandas_df.iloc[:, :10])  # Display the first 10 columns
            st.write(f"Full dataset contains {pandas_df.shape[0]} rows and {pandas_df.shape[1]} columns.")

            # Decrypt OpenAI key and store it in session state
            if 'open_ai_key' not in st.session_state:
                encrypted_val = b'gAAAAABm9fuEW69QQqx9iJj-d7mprLSD_YGeHMmK4MN91z_CwEAJ6YK9dC2v8_9OXfOVx2My8NV-whI0Nff-OG1iJCJcxh8Mvltm4ATeto4Gl8Rvph9JHbRsMEUHsfaFTmmvLXy0WBhwTIwfslvaytSkzk6kOEWNxjh8t4XZZKY3bebAptDnyNn2leK9tZIdRzTV1iiHym987eA-HmvmPx6RUdWrJHuP3W0g8OAgVG5cUJbth2WeAIM0K5IqBFqarvlvDw7RYVDPnPRy2pwq6VaGrzfTXZDQ4mf6wvQ8NHddIfvQbmPHqpE='
                key = cryptography_handler.load_key()
                open_ai_key = cryptography_handler.decrypt_api_key(encrypted_val, key)
                st.session_state['open_ai_key'] = open_ai_key

                os.environ["OPENAI_API_KEY"] = open_ai_key

        except Exception as e:
            st.error(f"An error occurred while loading the dataset: {str(e)}")
            logger.error("Error loading dataset: %s", str(e))

    # Check if dataset and API key are available in session state before allowing user input
    if 'pandas_df' in st.session_state and 'open_ai_key' in st.session_state:
        # Initialize Langchain agent
        llm = ChatOpenAI(model='gpt-4', temperature=0)
        agent = create_pandas_dataframe_agent(llm, st.session_state['pandas_df'], verbose=True, allow_dangerous_code=True)

        # Input text for user question
        user_question = st.text_input("Enter your question for the agent:", "What are the most correlated columns, choose 3")

        # Run the agent with the user question
        if st.button("Run Agent"):
            st.write("Running agent with your question...")
            try:
                response = agent.invoke(user_question)
                # Extract and display only the 'output' part of the response
                if isinstance(response, dict) and 'output' in response:
                    st.write(f"Agent Response: {response['output']}")
                else:
                    st.write(f"Unexpected response format: {response}")
            except Exception as e:
                st.error(f"An error occurred while running the agent: {str(e)}")
                logger.error("Error running agent: %s", str(e))

    # Add back button to return to the "Run Analysis" page
    if st.button("Go back to Run Analysis"):
        st.session_state.page = "run_analysis"

# Main app logic for handling page navigation
if st.session_state.page == "run_analysis":
    # Display the buttons side by side
    col1, col2 = st.columns([1, 1])
    
    with col1:
        run_analysis_page()
    
    with col2:
        if st.button("Dataset Analysis"):
            st.session_state.page = "dataset_analysis"
            
elif st.session_state.page == "dataset_analysis":
    dataset_analysis_page()
