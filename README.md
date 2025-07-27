📊 Data Analyser – AI-Powered RAG Streamlit App

Data Analyser is a Retrival‑Augmented Generation (RAG)–based data exploration tool built using Streamlit, Python, and modern Large Language Models (LLMs). Its goal is simple: make complex dataset analysis accessible to everyone. Just upload a CSV or Excel file, and the app generates rich insights—without any code. Powered by real-time data summarization, NLP, and AI-generated answers grounded in your data, Data Analyser turns raw tables into human-friendly conversations.

⸻

🌟 Motivation & Vision

In the data-driven world, CSV and Excel files are ubiquitous. Yet, deriving meaningful insights from them typically requires manual scripting, SQL queries, or deep spreadsheet expertise. This creates a barrier—especially for non-technical users like managers, researchers, and students.

Data Analyser bridges that gap by offering:
	•	📥 Zero-code data interaction: Upload a file, ask questions, get answers.
	•	🧠 AI-understanding of your data: Questions are natural language queries parsed by a fine-tuned LLM.
	•	⚡ Instant exploration: Preview data, compute summaries, detect trends and correlations—all on the fly.
	•	📚 Retrieval-Augmented Generation (RAG): Instead of generative hallucinations, responses are grounded in actual dataset content.

Ultimately, Data Analyser empowers anyone—technical or not—to “talk to their data”.

⸻

🧩 Architecture & Workflow

File Upload & Data Profiling
	1.	File Uploader: Accepts .csv or .xlsx files (max ~10 MB).
	2.	Data Parsing: Uses pandas to load and sanitize the dataset; supports fallback encodings like ISO-8859-1.
	3.	Column Summary: Computes df.info(), df.isna().sum(), data types, sample values for each column.
	4.	Preview Pane: Displays a table of first 10 rows and summary stats to users.

UI & Prompt Construction
	•	Suggested Questions UI (e.g. “Which column has missing data?”, “What is the average of numeric columns?”).
	•	Manual Query Input for custom natural language prompts.
	•	Session State Management: Maintains conversation history using st.session_state to store user and assistant messages, enabling full context in the session.

Model Interaction – RAG-Style

Data Analyser builds a prompt that includes:
	•	Column metadata (name, dtype, sample values)
	•	A small preview of data (up to 15 rows)
	•	The user query context

The prompt is then sent to a language model via huggingface’s InferenceClient (e.g. google/flan-t5-large). Rather than retrieving from external documents, prompt context is the actual dataset preview—so each answer is firmly grounded in your data.

Numeric Operations Channel

A “Quick Analysis” section enables one-click operations:
	•	Highest, Lowest, Average, Sum of selected numeric columns
	•	Performed via pandas and using simple UI elements

These operations augment the AI chat and provide immediate numeric insights.

Chat Interface

Built around Streamlit’s st.chat_message and st.chat_input (per Streamlit docs)  ￼ ￼ ￼.
User messages and AI responses are shown sequentially; entire conversation is scrollable and persistent within the session. Option to clear history is also provided.

⸻

🚀 Key Features & Capabilities

✔️ Instant Data Understanding
	•	Auto-detection of column types (numeric, categorical, datetime, string).
	•	Identification of missing values, sample rows, and column uniqueness.
	•	Summarizes dataset structure and potential anomalies in natural language.

✔️ Recommended Questions
	•	Eight preset analytical questions tailored to common exploratory tasks:
	•	“What are the top 5 highest values?”
	•	“Which column has missing data?”
	•	“What is the average of numeric columns?”

These cover trends, outliers, correlations, and broader dataset summaries.

✔️ Ask Your Own Questions
	•	Users can type free-form natural language queries like:
“Is there a correlation between columns A and B?”
“Which column has the most unique values?”
	•	Prompt is dynamically built to embed dataset context for accurate AI-generated responses.

✔️ Quick Numeric Operations
	•	Select a numeric column from a dropdown.
	•	Choose operations such as Highest, Lowest, Average, Sum.
	•	Get immediate computed output displayed with formatting icons (📈, 📉, 📊, 🧮).

✔️ Conversation History
	•	Maintains user-AI exchanges in session state with roles USER / ASSISTANT.
	•	Offers a “Clear History” button to reset the session context.
	•	Ensures context continuity if user asks follow-up questions.

✔️ Error Handling & Robustness
	•	Handles file loading via fallback encoding to accommodate edge cases.
	•	Wraps all AI calls and numeric operations in try/except blocks with error messages.
	•	Displays informative errors (via st.error) if model call fails or file parsing breaks.

✔️ Lightweight, Secure, and GDPR-friendly
	•	No persistent data storage—datasets are processed in-memory and discarded.
	•	Minimal dependencies and no sensitive SDKs or local service hosting.
	•	Suitable for local or cloud deployment with minimal configuration.

⸻

🧪 Data Security & Privacy
	•	Uploaded files are handled in-memory in the Streamlit session—never stored persistently.
	•	AI prompts include dataset previews but not full datasets beyond first 15 rows.
	•	No third-party tracking.
	•	Easily deployable locally for offline or private use—ideal for sensitive datasets.

⸻

📈 Use Cases & Audience

📊 Business Users & Analysts

Quickly explore CSV exports from ERPs, BI platforms, or customer datasets—without needing Excel formulas or SQL knowledge.

🎓 Students & Researchers

Upload experiment or survey data to generate insights and summaries in seconds—ideal for class assignments or early analysis.

🧪 Data Professionals

Use the app as a QA tool for verifying pipeline outputs, spot-checking sample files before ingestion into production systems.

📝 Managers & Executives

Get digestible summaries from reports in CSV form and ask intuitive questions like “Which region had the lowest sales?” without digging into spreadsheets.

⸻

🧠 Differentiators: Why Data Analyser Stands Out
	•	🔍 Context-Aware Answers: Every response is explicitly derived from the actual dataset—no generic guesses.
	•	🧩 Structured Prompting ensures that AI answers remain precise (subjected to column info and actual samples).
	•	🧪 Preset and custom queries together make the tool versatile yet user-friendly.
	•	⚡ Real-time operations for numeric metrics without invoking the AI (faster and more efficient).
	•	🗣️ Conversation continuity—AI can follow up based on user’s prior questions (while in same session).

⸻

🔮 Future Enhancements Roadmap

1. Custom Chart Generation
	•	Let the chatbot suggest and render plots (bar charts, scatter plots, box plots) using matplotlib or plotly.
	•	Downloadable charts for reporting or presentation.

2. Advanced Query Mode
	•	Allow free-form questions beyond the 8 preset buttons.
	•	Use prompt rewriting techniques to interpret user intent and adapt LLM prompts.

3. Dataset Cleaning Assistant
	•	Auto-detect columns with too many missing values or invalid entries.
	•	Suggest imputation options or drop columns—all powered by AI suggestion.

4. Multilingual Queries
	•	Accept queries in languages like Hindi, Spanish, etc., and translate prompts/responses accordingly.

5. Session Persistence & User Accounts
	•	Enable logged-in users to save conversation sessions, revisit past queries, or share insights.

6. Plugin System for File Types
	•	Support JSON, XML, Google Sheets, SQL exports, or database table loads.
	•	Extend prompt creator to support structured or semi-structured data.

7. Alternative Large Models or On-Premise Deployments
	•	Support open‑source LLMs hosted locally or through Docker for on-premise use—enhancing cost control and privacy.

⸻

✅ Summing It Up

Data Analyser transforms data understanding from a technical chore into an intuitive, conversational experience.
By combining Streamlit’s simplicity, LLM-powered question-answering, and structured dataset context, you can explore any CSV/Excel file—without writing code.

Whether you’re a beginner user or a data specialist, Data Analyser puts insights literally at your fingertips: upload, click a question, and explore.

⸻

📚 References & Inspiration
	•	Streamlit’s chat UI elements like st.chat_message and st.chat_input support seamless conversational interfaces  ￼
	•	RAG architecture provides factual grounding by including retrieved context with generative modeling—reducing AI hallucinations
	•	LangChain + Streamlit designs have shown effective prompt orchestration for custom document Q&A scenarios
