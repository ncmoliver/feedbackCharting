import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI# Assumed for LLM interaction
from dotenv import load_dotenv
import os
import re

load_dotenv(".env")
# OpenAI API Key (replace with your actual key or use environment variable)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
def perform_sentiment_analysis(response_text):
    """Uses an LLM to analyze sentiment from open-ended responses."""
    prompt = f"Analyze the sentiment of this response as positive, neutral, or negative: {response_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        sentiment = response["choices"][0]["message"]["content"].strip()
        return sentiment
    except Exception as e:
        return "Error"

st.title("Feedback Data Analysis")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    

    # Identify Yes/No Questions
    df_lower = df.map(lambda x: x.lower() if isinstance(x, str) else x)
    yes_no_cols = [
        col for col in df_lower.columns
    if df_lower[col].dropna().astype(str).isin(['yes', 'no']).all()
]
    with st.expander("### Preview of Yes/No Columns"):
        st.dataframe(yes_no_cols)

    # Function to identify question columns
    def is_question(column_name):
        """Check if a column name represents a question."""
        column_name = str(column_name).strip()  # Ensure it's a string
        question_words = ["what", "how", "why", "do", "is", "can", "will", "did", "are", "would", "could"]

        return column_name.endswith("?") or any(re.search(rf"\b{word}\b", column_name.lower()) for word in question_words)

    # Separate feature columns and question columns
    non_y_n_cols = [col for col in df.columns if col not in yes_no_cols]
    non_y_n_cols = pd.DataFrame(non_y_n_cols)
    with st.expander("### Preview of Non Yes/No Columns"):
        st.dataframe(non_y_n_cols)
   # Separate question and feature columns
    question_cols = [col for col in non_y_n_cols.columns if is_question(col)]
    feature_cols = [col for col in non_y_n_cols.columns if col not in question_cols]



    with st.expander("### Preview of Question Columns"):
        st.dataframe(question_cols)
    with st.expander("### Preview of Feature Columns"):
        st.dataframe(feature_cols)
    

        # # Display Charts for Yes/No Questions
        # for col in yes_no_cols:
        #     fig, ax = plt.subplots()
        #     df[col].value_counts().plot(kind='bar', ax=ax, color=['green', 'red'])
        #     ax.set_title(f'Responses for {col}')
        #     ax.set_ylabel("Count")
        #     st.pyplot(fig)

        # # Perform Sentiment Analysis on Open-ended Questions
        # if open_ended_cols:
        #     st.write("### Sentiment Analysis of Open-ended Responses")
        #     sentiment_results = {}
            
        #     for col in open_ended_cols:
        #         st.write(f"Processing Sentiments for: {col}")
        #         df[col] = df[col].astype(str)
        #         df[f"{col}_sentiment"] = df[col].apply(perform_sentiment_analysis)
        #         sentiment_results[col] = df[f"{col}_sentiment"].value_counts()
                
        #     # Save the processed data
        #     output_file = "processed_feedback_results.csv"
        #     df.to_csv(output_file, index=False)
        #     st.download_button("Download Processed Data", data=df.to_csv(index=False), file_name=output_file)

        #     # Display Sentiment Chart
        #     for col, sentiment_count in sentiment_results.items():
        #         fig, ax = plt.subplots()
        #         sentiment_count.plot(kind='bar', ax=ax, color=['blue', 'gray', 'orange'])
        #         ax.set_title(f'Sentiment Distribution for {col}')
        #         ax.set_ylabel("Count")
        #         st.pyplot(fig)

st.write("Upload a CSV file with Yes/No responses and open-ended questions for analysis.")
