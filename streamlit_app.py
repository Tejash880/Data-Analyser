import streamlit as st
import pandas as pd
import numpy as np
from huggingface_hub import InferenceClient
import time
from io import StringIO
import traceback

# --- Page setup ---
st.set_page_config(
    page_title="📊 Advanced RAG Data Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Hugging Face token and client initialization ---
HF_TOKEN = "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"  # Replace with your full token

try:
    MODEL_NAME = "google/flan-t5-large"
    client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)
except Exception as e:
    st.error(f"❗ Failed to initialize Hugging Face client: {e}")
    st.stop()

# --- Session state for conversation history ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Suggested questions ---
suggested_questions = [
    "What are the top 5 highest values?",
    "Which column has missing data?",
    "What trends can you observe?",
    "Is there any correlation between columns?",
    "What is the average of numeric columns?",
    "Summarize the dataset.",
    "Are there outliers?",
    "Which column has the most unique values?"
]

# --- Function to build prompt for LLM ---
def build_prompt(df_head, user_query):
    try:
        columns_info = "\n".join([
            f"- {col}: {df_head[col].dtype} (Sample: {df_head[col].iloc[0] if not df_head[col].empty else 'N/A'})"
            for col in df_head.columns
        ])
        return (
            "You are a professional data analyst. Here's a sample of the dataset:\n\n"
            f"Dataset Columns:\n{columns_info}\n\n"
            f"Sample Rows:\n{df_head.to_string(index=False, max_rows=15)}\n\n"
            f"User Question: {user_query}\n\n"
            "Provide a concise and accurate answer based on the data:"
        )
    except Exception as e:
        return f"⚠️ Prompt Error: {e}"

# --- Function to query Hugging Face LLM ---
def ask_llm(df, user_query):
    try:
        df_preview = df.head(15) if not df.empty else df
        prompt = build_prompt(df_preview, user_query)
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=100
        )
        return response.strip()
    except Exception as e:
        st.error(f"⚠️ LLM Error: {e}")
        st.text(traceback.format_exc())
        return f"⚠️ LLM Error: {e}"

# --- Quick numeric operations ---
def perform_operation(df, operation, column):
    try:
        if not pd.api.types.is_numeric_dtype(df[column]):
            return f"❌ Column '{column}' is not numeric."
        with st.spinner(f"Calculating {operation.lower()}..."):
            time.sleep(0.5)
            if operation == "Highest":
                return f"📈 Highest value in '{column}': {df[column].max()}"
            elif operation == "Lowest":
                return f"📉 Lowest value in '{column}': {df[column].min()}"
            elif operation == "Average":
                return f"📊 Average of '{column}': {round(df[column].mean(), 2)}"
            elif operation == "Sum":
                return f"🧮 Total sum of '{column}': {df[column].sum()}"
    except Exception as e:
        return f"⚠️ Calculation Error: {e}"

# --- Sidebar ---
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("""
    **Advanced Data Chatbot**  
    - Upload CSV/Excel datasets  
    - AI-powered data insights  
    - Quick numeric column analysis  
    """)
    st.divider()
    st.caption(f"Model: {MODEL_NAME}")

# --- Main App Interface ---
st.title("📊 Data Analysis Chatbot")
st.write("Upload your dataset to get started")

uploaded_file = st.file_uploader(
    "Choose a file (CSV or Excel)",
    type=["csv", "xlsx"],
    help="Max size: 10MB"
)

if uploaded_file:
    try:
        with st.spinner("Loading data..."):
            if uploaded_file.name.endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception:
                    df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.success("✅ Data loaded successfully!")

        # Tabs for preview and summary
        tab_preview, tab_summary = st.tabs(["📄 Data Preview", "🔍 Data Summary"])
        with tab_preview:
            st.dataframe(df.head(10), use_container_width=True)
        with tab_summary:
            buffer = StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            st.text(info_str)
            st.write("Missing values per column:")
            st.write(df.isna().sum())

        st.divider()

        # Layout for quick analysis and chat interaction
        col1, col2 = st.columns([0.3, 0.7])

        with col1:
            st.subheader("🔢 Quick Analysis")
            action = st.selectbox(
                "Choose operation:",
                ["Ask a question", "Highest", "Lowest", "Average", "Sum"]
            )

            if action == "Ask a question":
                manual_query = st.text_area(
                    "Enter your question:",
                    placeholder="e.g., What is the correlation between column A and B?",
                    height=100
                )
                if st.button("Ask", key="manual_ask_button") and manual_query:
                    with st.spinner("Analyzing your question..."):
                        answer = ask_llm(df, manual_query)
                        st.session_state.conversation.append(("USER", manual_query))
                        st.session_state.conversation.append(("ASSISTANT", answer))
                        st.rerun()
            else:
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                if numeric_cols:
                    selected_col = st.selectbox("Select column:", numeric_cols)
                    if st.button("Calculate", key="calc_button"):
                        result = perform_operation(df, action, selected_col)
                        st.session_state.conversation.append(("SYSTEM", result))
                        st.rerun()
                else:
                    st.warning("No numeric columns available.")

        with col2:
            st.subheader("💬 Chat with Data")
            st.write("Click a question to ask:")

            cols = st.columns(4)
            for i, question in enumerate(suggested_questions):
                if cols[i % 4].button(question, key=f"suggested_{i}"):
                    with st.spinner("Analyzing..."):
                        answer = ask_llm(df, question)
                        st.session_state.conversation.append(("USER", question))
                        st.session_state.conversation.append(("ASSISTANT", answer))
                        st.rerun()

        st.divider()
        st.subheader("💭 Ask Your Own Question")
        if prompt := st.chat_input("Type your question about the data here..."):
            with st.spinner("Analyzing your question..."):
                answer = ask_llm(df, prompt)
                st.session_state.conversation.append(("USER", prompt))
                st.session_state.conversation.append(("ASSISTANT", answer))
                st.rerun()

        st.divider()
        st.subheader("📚 History")
        if st.session_state.conversation:
            if st.button("🗑️ Clear History", key="clear_history"):
                st.session_state.conversation = []
                st.rerun()

        if not st.session_state.conversation:
            st.info("No interactions yet.")
        else:
            for speaker, message in st.session_state.conversation:
                if speaker == "USER":
                    st.markdown(f"**You:** {message}")
                elif speaker == "ASSISTANT":
                    st.markdown(f"**AI:** {message}")
                    st.divider()
                else:
                    st.success(message)

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

else:
    st.info("⬆️ Please upload a CSV or Excel file")
