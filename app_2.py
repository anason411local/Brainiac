import streamlit as st
from agent.langgraph_agent import get_rag_agent

# Set up Streamlit page layout
st.set_page_config(page_title="Winback RAG Assistant", layout="wide")

# Title and instruction
st.title("📾 Winback AI Assistant")
st.markdown("Ask questions about customer journeys, objections, cancellations, and successful campaigns.")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Load RAG agent
qa = get_rag_agent()

# Welcome message
with st.chat_message("ai"):
    st.markdown("How can I help with your Winback customer today?")

# Get user query
query = st.chat_input("Ask about a customer...")

# Run RAG and show result in ui
if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking..."):
        result = qa.invoke({"query": query})
        answer = result["result"]

    with st.chat_message("ai"):
        st.markdown(answer)

    # Save chat
    st.session_state.history.append({"question": query, "answer": answer})