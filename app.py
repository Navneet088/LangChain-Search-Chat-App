import time
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.tools import Tool
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType

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

# ---------- Page Config ----------

st.set_page_config(page_title="LangChain Search Chat", page_icon="🔎")
st.title("🔎 LangChain - Chat with Search")

# ---------- Sidebar ----------

st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown("**Tools Available:**")
st.sidebar.markdown("- 📖 Wikipedia\n- 📄 Arxiv\n- 🌐 DuckDuckGo")

# ---------- Session State ----------

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I can search Wikipedia, Arxiv and the web. What would you like to know?"}
    ]

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )

# ---------- Chat History ----------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- Chat Input ----------

if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
        st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Build LLM + Agent
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        streaming=True
    )

    agent = initialize_agent(
        tools=[wiki, arxive, search],   # wiki & arxiv first = tried first
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

    # Run agent and show response
    with st.chat_message("assistant"):
        cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = agent.run(prompt, callbacks=[cb])
        except Exception as e:
            response = "Sorry, something went wrong. Please try again."
            st.error(str(e))
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})







