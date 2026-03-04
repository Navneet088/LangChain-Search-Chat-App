# 🔎 LangChain Search Chat

> **A conversational AI agent that searches Wikipedia, Arxiv & the web in real time**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain_Agents-🤖-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-FF6B35?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ReAct](https://img.shields.io/badge/ReAct-Framework-7C3AED?style=for-the-badge)

---

## 📌 Overview

**LangChain Search Chat** is an end-to-end conversational AI agent that searches **Wikipedia**, **Arxiv research papers**, and the **live web via DuckDuckGo** — all in one chat interface.

Built on the **ReAct agent framework** with persistent memory, it reasons about which tool to use before acting, and **streams its thought process live** in the UI so you can see exactly how it reached its answer.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🧠 **ReAct Agent** | `ZERO_SHOT_REACT_DESCRIPTION` — reasons step-by-step: Thought → Action → Observation |
| 🔢 **Iteration Cap** | `max_iterations=2` hard-limits tool calls; `early_stopping_method=generate` ensures graceful finish |
| 🛡️ **Error Recovery** | `handle_parsing_errors=True` recovers from malformed LLM output without crashing |
| 📖 **Wikipedia Tool** | Top 3 results, up to 3,000 chars each — best for general knowledge |
| 📄 **Arxiv Tool** | Top 2 research papers, 1,500 chars each — activated for academic queries |
| 🌐 **DuckDuckGo Tool** | Live web search with **3-second rate-limit cooldown guard** and graceful fallback |
| 🔖 **Tool Tracker** | `make_tracked_tool()` closure logs exactly which tools fired each turn |
| 🏷️ **Colour-Coded Badges** | Inline HTML badges (📖 Wikipedia / 📄 Arxiv / 🌐 DuckDuckGo) shown under each reply |
| 💾 **Persistent Memory** | `ConversationBufferMemory` stored in `st.session_state` — survives Streamlit reruns |
| 📡 **Live Streaming** | `StreamlitCallbackHandler` streams agent thoughts and tool calls in real time |
| 🤖 **Model Selector** | 4 Groq-hosted models selectable in sidebar |
| 🗑️ **Clear Chat** | Resets messages, memory, and tool history atomically, then calls `st.rerun()` |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — chat UI with session state management
- **LangChain** — agent orchestration (`initialize_agent`, `AgentType`, `Tool`)
- **langchain-groq** — Llama 3.3-70B / 3.1-8B / Mixtral / Gemma2 via Groq
- **langchain-community** — `WikipediaQueryRun`, `ArxivQueryRun`, `DuckDuckGoSearchRun`
- **ConversationBufferMemory** — multi-turn context persistence
- **StreamlitCallbackHandler** — live streaming of agent reasoning

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langchain-search-chat.git
cd langchain-search-chat
```

### 2. Install dependencies

```bash
pip install streamlit langchain langchain-groq langchain-community
pip install wikipedia arxiv duckduckgo-search
```

### 3. Run the app

```bash
streamlit run app.py
```

> Enter your **Groq API key** in the sidebar when the app opens.

---

## 📖 How to Use

1. Enter your **Groq API key** in the sidebar
2. Select a model (`llama-3.3-70b-versatile` recommended for best accuracy)
3. Type any question in the chat input
4. Watch the agent **think in real time** — it picks the right tool automatically
5. Colour-coded **tool badges** show which sources were used for each answer
6. Use **"Clear Chat History"** to start a fresh session

---

## 🏗️ How It Works

```
User Query
   │
   ▼
ReAct Agent (ZERO_SHOT_REACT_DESCRIPTION)
   │
   ├─ Thought: "What do I need to find?"
   ├─ Action:  picks best tool (or skips if it already knows)
   │
   ├──▶ 📖 WikipediaQueryRun    (general knowledge)
   ├──▶ 📄 ArxivQueryRun        (research papers)
   └──▶ 🌐 DuckDuckGoSearchRun  (live web / news)
         │
         ▼
   Observation (tool result)
         │
         ▼
   Final Answer → streamed to Streamlit UI
         │
         ▼
   Tool badges rendered + saved to session memory
```

---

## 🗺️ Tool Routing Guide

| Query Type | Tool Used |
|-----------|-----------|
| General knowledge, history, people | 📖 Wikipedia — fast, reliable, no rate limits |
| Research papers, science, academia | 📄 Arxiv — abstracts and author info |
| Current events, recent news | 🌐 DuckDuckGo — live web, real-time data |
| Simple facts (capitals, dates, math) | 🤖 No tool — answered directly from LLM |

---

## 🤖 Available Models

| Model | Best For |
|-------|----------|
| `llama-3.3-70b-versatile` | Best instruction-following, most accurate ✅ |
| `llama-3.1-8b-instant` | Fast and lightweight queries ⚡ |
| `mixtral-8x7b-32768` | Long context tasks 📄 |
| `gemma2-9b-it` | Lightweight alternative 🪶 |

---

## 🐛 Known Issue & Fix

> **Bug:** The file ends mid-line at `st.session_state.tools_used.append(t` — the `tools_this_turn` list is never saved. Tool badges won't render on page reload for the final assistant reply.

**Fix — complete the line as:**

```python
st.session_state.tools_used.append(list(tools_this_turn))
```

---

## 💡 Pro Tips

> - Use `llama-3.3-70b-versatile` for the best results on complex, multi-step queries.
> - The **3-second DuckDuckGo cooldown is intentional** — removing it causes rate-limit errors.
> - The agent skips tools for simple facts it already knows — this is by design (faster + cheaper).

---

## 📁 Project Structure

```
langchain-search-chat/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📦 requirements.txt

```
streamlit
langchain
langchain-groq
langchain-core
langchain-community
wikipedia
arxiv
duckduckgo-search
```

---

> Built with ❤️ using **LangChain · Groq · Streamlit**

## 🎯 Features

- 💬 Interactive Chat Interface (Streamlit)
- 🧠 ZERO_SHOT_REACT LangChain Agent
- 🔍 Real-time Web Search
- 📖 Wikipedia Knowledge Retrieval
- 📚 Arxiv Research Paper Search
- ⚡ Streaming LLM Responses
- 🔄 Live Agent Reasoning Display
- 🗂️ Session-based Chat Memory

---

## 🏗️ Architecture

User Query  
   ↓  
LangChain Agent  
   ↓  
Tool Selection  
   ↓  
(Wikipedia | Arxiv | DuckDuckGo)  
   ↓  
Groq LLM Response  
   ↓  
Streamlit Chat Output  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LangChain  
- LangChain Community Tools  
- Groq API  
- DuckDuckGo Search  
- Wikipedia API  
- Arxiv API  
- python-dotenv  

---

## 📂 Project Structure
👨‍💻 Author

Navneet Kumar Jha
AI/ML & Web Development Enthusiast

📜 License

This project is for educational and demonstration purposes.


---

This version is:

- ✅ Clean  
- ✅ Professional  
- ✅ GitHub ready  
- ✅ Proper spacing  
- ✅ Proper code blocks  
- ✅ Good section hierarchy  

If you want, I can now make it **next-level premium GitHub style with badges + screenshots section + demo link section** 😎
