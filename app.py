import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page Config
st.set_page_config(page_title="🧠 AI Feedback Summarizer", layout="centered")

# Header
st.markdown("""
    <h1 style='text-align: center;'>🧠 AI Feedback Summarizer</h1>
    <p style='text-align: center; font-size: 18px;'>Upload user feedback (CSV) and generate smart summaries using GPT-4</p>
""", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader("📄 Upload a CSV file (must include a feedback column)", type="csv")

# GPT Logic
def generate_insights(feedback_list, batch_size=20):
    def summarize_batch(batch):
        prompt = (
            "You are a product strategist. Analyze the following user feedback. "
            "Group them into 3–5 key themes. For each theme, give a short summary and include 1–2 user quotes.\n\n"
            "User feedback:\n" + "\n".join(f"- {item}" for item in batch)
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

    batches = [feedback_list[i:i + batch_size] for i in range(0, len(feedback_list), batch_size)]
    batch_summaries = []
    progress = st.progress(0)

    for idx, batch in enumerate(batches):
        st.write(f"🔍 Processing batch {idx + 1} of {len(batches)}...")
        summary = summarize_batch(batch)
        batch_summaries.append(f"### Batch {idx+1}\n{summary}")
        progress.progress((idx + 1) / len(batches))

    final_prompt = (
        "You're a product strategist. The following are summaries of customer feedback batches. "
        "Please combine them into a single, concise insight summary with 3–5 key themes and 1–2 quotes per theme.\n\n"
        + "\n\n".join(batch_summaries)
    )

    final_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and concise product strategist."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )
    return final_response.choices[0].message.content

# Run app
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    columns = df.columns.tolist()
    selected_column = st.selectbox("📝 Select the column containing feedback", columns)

    if st.button("🚀 Generate Insights"):
        feedback_list = df[selected_column].dropna().astype(str).tolist()
        with st.spinner("Analyzing feedback using GPT..."):
            insights = generate_insights(feedback_list)

        st.subheader("📊 Key Insights")
        st.markdown(insights)

        # Download button
        filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        st.download_button("📥 Download Summary", insights, file_name=filename)
