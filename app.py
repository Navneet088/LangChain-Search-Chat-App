#All importent Librery
import streamlit as st 
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.tools  import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv
load_dotenv()




#use Arxive ,wikipedia and duckrun toll to search
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=5,doc_content_chars_max=2000)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)


api_wrapper_arxive = ArxivAPIWrapper(top_k_results=5,doc_content_chars_max=2000)
arxive = ArxivQueryRun(api_wrapper=api_wrapper_arxive)

api_wrapper_ddg = DuckDuckGoSearchAPIWrapper(max_results=5)
search = DuckDuckGoSearchRun(api_wrapper=api_wrapper_ddg)
memory = ConversationBufferMemory(memory_key="chat_history")

st.title("🔎 LangChain -Chat with Search")
st.markdown("""
### 🚀 About This App

This application demonstrates how to use **LangChain Agents**  
with **StreamlitCallbackHandler** to show:

- 🧠 Agent reasoning  ⚙️ Tool usage  🔍 Intermediate steps  

All displayed live inside a Streamlit interface.

""")

## input the groq api key
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter Groq API Key:",type="password")

# Initialize session history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a chatbot who can search the web. How can I help you?"
        }
    ]

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


if prompt := st.chat_input("Ask something"):

    if not api_key:
        st.warning("Please enter Groq API Key")
        st.stop()

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Create LLM
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        streaming=True
    )

    tools = [search, arxive, wiki]

    search_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        handling_parsing_errors=True
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        respounce=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.write(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})








