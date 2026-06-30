import os
import logging
import time
import streamlit as st
from dotenv import load_dotenv
import sys

from multi_agent_app.orchestrator import select_and_run_agent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .agent-tavily { background-color: #e3f2fd; color: #1565c0; }
    .agent-aviation { background-color: #fce4ec; color: #c2185b; }
    .agent-weather { background-color: #e8f5e9; color: #2e7d32; }
    .agent-ecommerce { background-color: #fff3e0; color: #ef6c00; }
    .agent-football { background-color: #f3e5f5; color: #7b1fa2; }
    .agent-ipl { background-color: #fff8e1; color: #f57f17; }
    .response-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "use_groq" not in st.session_state:
    st.session_state.use_groq = True

# Header
st.markdown('<div class="main-header">🤖 Multi-Agent AI Assistant</div>', unsafe_allow_html=True)

st.markdown("""
This multi-agent system uses specialized AI agents to handle different types of queries:
- **Web Search Agent** (Tavily): General web searches, news, research
- **Aviation Agent** (AviationStack): Flight status, airport information
- **Weather Agent** (OpenWeather): Current weather, forecasts
- **E-commerce Agent** (ECOMMERCE_DB): Orders, products, reviews, customers
- **Football Agent** (ETL_PIPELINES_DB): Players, matches, teams, leagues
- **IPL Cricket Agent** (ETL_PIPELINES_DB): IPL matches, players, teams, statistics
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # LLM Selection
    st.subheader("LLM Provider")
    use_groq = st.radio(
        "Select LLM Provider",
        ["Groq (Llama3)", "OpenAI (GPT-4o-mini)"],
        index=0 if st.session_state.use_groq else 1
    )
    if use_groq != ("Groq (Llama3)" if st.session_state.use_groq else "OpenAI (GPT-4o-mini)"):
        logger.info(f"LLM provider changed to: {use_groq}")
    st.session_state.use_groq = (use_groq == "Groq (Llama3)")
    
    # Warning for Groq
    if st.session_state.use_groq:
        st.warning("⚠️ Groq may have tool calling limitations. OpenAI (GPT-4o-mini) is recommended for better compatibility with tool-based agents.")
    
    # API Key Status
    st.subheader("API Key Status")
    api_keys = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
        "AVIATIONSTACK_API_KEY": os.getenv("AVIATIONSTACK_API_KEY"),
        "OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY"),
        "POSTGRES_DB_URL": os.getenv("POSTGRES_DB_URL"),
    }
    
    for key, value in api_keys.items():
        status = "✅" if value else "❌"
        st.text(f"{status} {key}")
    
    # Database Connection Info
    st.subheader("Database Connections")
    st.text("Football DB: ETL_PIPELINES_DB.public")
    st.text("E-commerce DB: ECOMMERCE_DB.SILVER")
    st.text("IPL DB: ETL_PIPELINES_DB.SILVER")
    
    # Clear chat button
    if st.button("Clear Chat History"):
        logger.info("Clear Chat History button clicked")
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            agent_name = message.get("agent", "Unknown Agent")
            st.markdown(f'<span class="agent-badge agent-{agent_name.lower().split()[0]}">{agent_name}</span>', unsafe_allow_html=True)
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    logger.info(f"User submitted query: {prompt[:100]}...")
    start_time = time.time()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Processing your query..."):
            try:
                logger.info(f"Processing query with use_groq={st.session_state.use_groq}")
                agent_name, response = select_and_run_agent(
                    prompt,
                    use_groq=st.session_state.use_groq
                )
                
                end_time = time.time()
                duration = end_time - start_time
                logger.info(f"Query processed successfully by {agent_name} in {duration:.2f} seconds")
                
                # Display agent badge
                st.markdown(f'<span class="agent-badge agent-{agent_name.lower().split()[0]}">{agent_name}</span>', unsafe_allow_html=True)
                
                # Display response
                st.markdown(response)
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "agent": agent_name
                })
                
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                logger.error(f"Error processing query after {duration:.2f} seconds: {(str(e))}")
                error_message = f"Error processing your query: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "agent": "System"
                })

# Example queries
st.divider()
st.subheader("💡 Example Queries")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Web Search:**")
    st.code("Search for latest AI trends", language="text")
    st.markdown("**Weather:**")
    st.code("What's the weather in London?", language="text")

with col2:
    st.markdown("**Aviation:**")
    st.code("Check flight status for BA123", language="text")
    st.markdown("**E-commerce:**")
    st.code("Show me total revenue", language="text")

with col3:
    st.markdown("**Football:**")
    st.code("How many players in the database?", language="text")
    st.code("Get match statistics", language="text")
    st.markdown("**IPL Cricket:**")
    st.code("Show top run scorers", language="text")
    st.code("Get team performance", language="text")
