# 🧠 AI Feedback Summarizer

AI Feedback Summarizer is a Streamlit web app that uses GPT-4 to analyze and summarize large sets of user feedback into clear, actionable insights — perfect for product managers, researchers, and startup teams.

---

## 🚀 Features

- 📤 Upload a CSV with user feedback
- 🧠 Uses GPT-4 to group insights into 3–5 key themes
- 💬 Includes real user quotes under each theme
- ⚙️ Automatically handles large files via smart batching


---

## 📂 How It Works

1. Upload a CSV file with a `feedback` or `comments` column
2. App batches the feedback into smaller chunks
3. GPT-4 processes each batch, summarizes, and then merges them
4. Displays a clean, final summary with grouped insights

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io)
- [OpenAI API](https://platform.openai.com/)
- [Python](https://www.python.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/kiranksibi/ai-feedback-summarizer.git
   cd ai-feedback-summarizer
