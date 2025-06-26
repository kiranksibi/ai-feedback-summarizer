import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env or sidebar
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



# Initialize client
client = OpenAI()

# ----------------------------
# GPT Function
# ----------------------------
def generate_insights(feedback_list):
    prompt = (
        "You are a product strategist. Analyze the following user feedback. "
        "Group them into 3–5 key themes. For each theme, give a short summary and include 1–2 user quotes.\n\n"
        "User feedback:\n"
        + "\n".join(f"- {item}" for item in feedback_list)
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful and concise product strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content

# ----------------------------
# Streamlit App UI
# ----------------------------
st.set_page_config(page_title="AI Feedback Summarizer", layout="wide")
st.title("🧠 AI Feedback Summarizer")
st.write("Upload customer feedback and get grouped insights using GPT.")

# File upload
uploaded_file = st.file_uploader("📄 Upload a CSV file (must include a 'feedback' column)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'feedback' not in df.columns:
        st.error("⚠️ Your CSV must contain a column named 'feedback'.")
    else:
        st.success("✅ File uploaded successfully!")
        st.write("Here’s a preview of your data:")
        st.dataframe(df.head())

        # Generate GPT insights
        if st.button("🚀 Generate Insights"):
            feedback_list = df['feedback'].dropna().tolist()

            with st.spinner("Analyzing feedback using GPT..."):
                try:
                    insights = generate_insights(feedback_list)
                    st.subheader("🧠 Key Insights")
                    st.markdown(insights)
                except Exception as e:
                    st.error(f"❌ Error generating insights: {e}")
