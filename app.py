#All importent Librery
import streamlit as st 
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.tools  import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv
load_dotenv()




#use Arxive ,wikipedia and duckrun toll to search
api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=5,doc_content_chars_max=2000)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)


api_wrapper_arxive = ArxivAPIWrapper(top_k_results=5,doc_content_chars_max=2000)
arxive = ArxivQueryRun(api_wrapper=api_wrapper_arxive)

search=DuckDuckGoSearchRun(name="Search")

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

if "messagess" not in st.session_state:
    st.session_state["messages"]=[
        {
           "role": "assisstant","content":"Hi,I'am a ChatBort Who can Search the Web .Hoe Can  I Help you? "

        }
    ]
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder="What is machin Learning ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt) 

    llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.1-8b-instant",streaming=True)
    tools=[search,arxive,wiki]
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        respounce=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assistant","content":respounce})
        st.write(respounce)


