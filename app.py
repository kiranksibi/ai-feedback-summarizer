import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# GPT Function: Summarize Feedback
# ----------------------------
def generate_insights(feedback_list):
    prompt = (
        "You are a product strategist. Analyze the following user feedback. "
        "Group them into 3–5 key themes. For each theme, give a short summary and include 1–2 user quotes.\n\n"
        "User feedback:\n"
        + "\n".join(f"- {item}" for item in feedback_list)
    )

    response = client.chat.completions.create(
        model="gpt-4",
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

# File uploader
uploaded_file = st.file_uploader("📄 Upload a CSV file (must include a column like 'comments' or 'feedback')", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.write("Here’s a preview of your data:")
    st.dataframe(df.head())

    # Select text column
    selected_column = st.selectbox("📝 Choose the column with feedback/comments", df.columns)

    if st.button("🚀 Generate Insights"):
        try:
            feedback_list = df[selected_column].dropna().tolist()
            with st.spinner("Analyzing feedback using GPT..."):
                insights = generate_insights(feedback_list)
            st.subheader("🧠 Key Insights")
            st.markdown(insights)
        except Exception as e:
            st.error(f"❌ Error: {e}")
