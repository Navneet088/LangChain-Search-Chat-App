# import time
# import streamlit as st
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.tools import Tool
# from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, ArxivAPIWrapper
# from langchain.memory import ConversationBufferMemory
# from langchain_groq import ChatGroq
# from langchain.agents import initialize_agent, AgentType

# # ---------- Tools Setup ----------

# wiki = WikipediaQueryRun(
#     api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
# )

# arxive = ArxivQueryRun(
#     api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
# )

# _ddg_last_called = {"time": 0}

# def safe_ddg_search(query: str) -> str:
#     elapsed = time.time() - _ddg_last_called["time"]
#     if elapsed < 3:
#         time.sleep(3 - elapsed)
#     try:
#         result = DuckDuckGoSearchRun(
#             api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=2)
#         ).run(query)
#         _ddg_last_called["time"] = time.time()
#         return result
#     except Exception:
#         return "DuckDuckGo is rate-limited. Rely on Wikipedia or Arxiv for this query."

# search = Tool(
#     name="duckduckgo_search",
#     func=safe_ddg_search,
#     description="Use ONLY for very recent news not found in Wikipedia or Arxiv."
# )

# # ---------- Page Config ----------

# st.set_page_config(page_title="LangChain Search Chat", page_icon="🔎")
# st.title("🔎 LangChain - Chat with Search")

# # ---------- Sidebar ----------

# st.sidebar.title("⚙️ Settings")
# api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
# st.sidebar.markdown("---")
# st.sidebar.markdown("**Tools Available:**")
# st.sidebar.markdown("- 📖 Wikipedia\n- 📄 Arxiv\n- 🌐 DuckDuckGo")

# # ---------- Session State ----------

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "assistant", "content": "Hi! I can search Wikipedia, Arxiv and the web. What would you like to know?"}
#     ]

# if "memory" not in st.session_state:
#     st.session_state["memory"] = ConversationBufferMemory(
#         memory_key="chat_history", return_messages=True
#     )

# # ---------- Chat History ----------

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# # ---------- Chat Input ----------

# if prompt := st.chat_input("Ask me anything..."):
#     if not api_key:
#         st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
#         st.stop()

#     # Show user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     # Build LLM + Agent
#     llm = ChatGroq(
#         groq_api_key=api_key,
#         model_name="llama-3.1-8b-instant",
#         streaming=True
#     )

#     agent = initialize_agent(
#         tools=[wiki, arxive, search],   # wiki & arxiv first = tried first
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         memory=st.session_state["memory"],
#         handle_parsing_errors=True,
#         max_iterations=3,
#         early_stopping_method="generate",
#         agent_kwargs={
#             "prefix": (
#                 "You are a helpful assistant. "
#                 "Use Wikipedia first, then Arxiv for research topics, "
#                 "and DuckDuckGo only for very recent news. "
#                 "Never call the same tool twice. "
#                 "Once you have enough info, give your Final Answer immediately."
#             )
#         }
#     )

#     # Run agent and show response
#     with st.chat_message("assistant"):
#         cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
#         try:
#             response = agent.run(prompt, callbacks=[cb])
#         except Exception as e:
#             response = "Sorry, something went wrong. Please try again."
#             st.error(str(e))
#         st.write(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})
import time
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.tools import Tool
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType

# ---------- Page Config ----------

st.set_page_config(page_title="LangChain Search Chat", page_icon="🔎", layout="centered")

# ---------- Session State Defaults ----------

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I can search Wikipedia, Arxiv and the web. What would you like to know?"}]
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
if "tools_used" not in st.session_state:
    st.session_state["tools_used"] = []

# ---------- Sidebar ----------

with st.sidebar:
    st.title("⚙️ Settings")

    # API Key
    api_key = st.text_input("🔑 Groq API Key:", type="password")

    st.markdown("---")

    # Model selector
    model = st.selectbox(
        "🤖 Select LLM Model",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        help="Larger models give better answers but are slower."
    )

    st.markdown("---")

    # Tools info
    st.markdown("**🛠️ Tools Available**")
    st.markdown("""
    - 📖 **Wikipedia** — general knowledge  
    - 📄 **Arxiv** — research papers  
    - 🌐 **DuckDuckGo** — recent news  
    """)

    st.markdown("---")

    # Clear chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["messages"] = [{"role": "assistant", "content": "Chat cleared! How can I help you?"}]
        st.session_state["memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        st.session_state["tools_used"] = []
        st.rerun()

# ---------- Title ----------

st.title("🔎 LangChain - Chat with Search")

# ---------- Tool Badge Helper ----------

def tool_badge(name: str) -> str:
    mapping = {
        "wikipedia":         ("📖 Wikipedia",   "background-color:#e8f4fd;color:#1a6fa0;"),
        "arxiv":             ("📄 Arxiv",        "background-color:#edf7ed;color:#2e7d32;"),
        "duckduckgo_search": ("🌐 DuckDuckGo",   "background-color:#fff3e0;color:#e65100;"),
    }
    label, style = mapping.get(name.lower(), (f"🔧 {name}", "background-color:#f3e5f5;color:#6a1b9a;"))
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:12px;'
        f'font-size:12px;font-weight:600;margin:2px;{style}">{label}</span>'
    )

# ---------- Tools Setup ----------

wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
)
arxive = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500)
)

_ddg_last_called = {"time": 0}

def safe_ddg_search(query: str) -> str:
    elapsed = time.time() - _ddg_last_called["time"]
    if elapsed < 3:
        time.sleep(3 - elapsed)
    try:
        result = DuckDuckGoSearchRun(
            api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=2)
        ).run(query)
        _ddg_last_called["time"] = time.time()
        return result
    except Exception:
        return "DuckDuckGo is rate-limited. Rely on Wikipedia or Arxiv for this query."

search = Tool(
    name="duckduckgo_search",
    func=safe_ddg_search,
    description="Use ONLY for very recent news not found in Wikipedia or Arxiv."
)

# ---------- Chat History ----------

tool_idx = 0
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and tool_idx < len(st.session_state.tools_used):
            tools = st.session_state.tools_used[tool_idx]
            if tools:
                badges = "".join(tool_badge(t) for t in tools)
                st.markdown(f"<small>🛠️ Tools used: {badges}</small>", unsafe_allow_html=True)
            tool_idx += 1

# ---------- Chat Input ----------

if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    llm = ChatGroq(groq_api_key=api_key, model_name=model, streaming=True)

    tools_this_turn = []

    def make_tracked_tool(t):
        original_func = t.func if hasattr(t, "func") else t.run
        def tracked(query, _name=t.name):
            tools_this_turn.append(_name)
            return original_func(query)
        return Tool(name=t.name, func=tracked, description=t.description)

    tracked_tools = [make_tracked_tool(t) for t in [wiki, arxive, search]]

    agent = initialize_agent(
        tools=tracked_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=st.session_state["memory"],
        handle_parsing_errors=True,
        max_iterations=3,
        early_stopping_method="generate",
        agent_kwargs={
            "prefix": (
                "You are a helpful assistant. "
                "Use Wikipedia first, then Arxiv for research topics, "
                "and DuckDuckGo only for very recent news. "
                "Never call the same tool twice. "
                "Once you have enough info, give your Final Answer immediately."
            )
        }
    )

    with st.chat_message("assistant"):
        cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = agent.run(prompt, callbacks=[cb])
        except Exception as e:
            response = "Sorry, something went wrong. Please try again."
            st.error(str(e))

        st.write(response)

        if tools_this_turn:
            badges = "".join(tool_badge(t) for t in tools_this_turn)
            st.markdown(f"<small>🛠️ Tools used: {badges}</small>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.tools_used.append(tools_this_turn)









