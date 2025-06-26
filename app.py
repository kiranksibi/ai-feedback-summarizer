import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Optional: Let user manually enter key (overrides .env if provided)
st.sidebar.title("🔐 Settings")
openai_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if openai_key:
    client = OpenAI(api_key=openai_key)

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
uploaded_file = st.file_uploader("📄 Upload a CSV file (should contain a 'feedback' or 'comments' column)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.write("Here’s a preview of your data:")
    st.dataframe(df.head())

    # Let user select the text column
    selected_column = st.selectbox("🔎 Choose the column with feedback/comments", df.columns)

    if selected_column:
        # Generate GPT insights
        if st.button("🚀 Generate Insights"):
            feedback_list = df[selected_column].dropna().tolist()

            with st.spinner("Analyzing feedback using GPT..."):
                try:
                    insights = generate_insights(feedback_list)
                    st.subheader("🧠 Key Insights")
                    st.markdown(insights)
                except Exception as e:
                    st.error(f"❌ Error generating insights: {e}")
