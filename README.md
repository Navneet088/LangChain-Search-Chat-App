🔎 LangChain Search Chat App

A Streamlit-based AI chatbot that can search the web using LangChain Agents and external tools like Wikipedia, Arxiv, and DuckDuckGo.

This app demonstrates how to integrate:

🧠 LangChain Agents

🔍 Web Search Tools

⚙️ Tool Reasoning with Callbacks

💬 Streamlit Chat Interface

🚀 Groq LLM (LLaMA 3.1)

📌 Features

✅ Chat-based interface using Streamlit

✅ Live agent reasoning with StreamlitCallbackHandler

✅ Uses multiple search tools:

Wikipedia

Arxiv Research Papers

DuckDuckGo Web Search

✅ Groq LLM integration (LLaMA 3.1 8B Instant)

✅ Displays intermediate tool usage steps

✅ Maintains chat session history

🛠️ Technologies Used

Python

Streamlit

LangChain

Groq API

DuckDuckGo Search

Wikipedia API

Arxiv API

dotenv

📂 Project Structure
project-folder/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
🔧 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/langchain-search-chat.git
cd langchain-search-chat
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt

Or manually:

pip install streamlit langchain langchain-community langchain-groq python-dotenv duckduckgo-search wikipedia arxiv
🔑 Setup Groq API Key

Get your API key from Groq.

Create a .env file in your root directory:

GROQ_API_KEY=your_api_key_here

OR enter the API key directly from the Streamlit sidebar input.

▶️ Run the Application
streamlit run app.py

The app will open in your browser.

🧠 How It Works

User enters a query in the chat.

LangChain Agent processes the query.

Agent decides which tool to use:

Wikipedia → General knowledge

Arxiv → Research papers

DuckDuckGo → Web search

Intermediate reasoning steps are displayed.

Final answer is returned in the chat.

🔎 Tools Used
📖 WikipediaQueryRun

Fetches summarized information from Wikipedia.

📚 ArxivQueryRun

Searches and retrieves research papers from Arxiv.

🌐 DuckDuckGoSearchRun

Performs real-time web search.

🖼️ UI Preview

Chat-based conversation

Sidebar for API key input

Live reasoning display

Clean Streamlit layout

🚀 Future Improvements

Add memory support

Add conversation summarization

Add multi-model selection

Add PDF upload support

Add vector database integration

📜 License

This project is for educational and demonstration purposes.
