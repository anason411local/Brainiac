import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores.weaviate import Weaviate
from vectorstore.weaviate_client import get_weaviate_client

# Load environment variables from .env
load_dotenv()

def get_rag_agent():
    # Load Gemini model
    gemini = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.4,
        convert_system_message_to_human=True,
        max_output_tokens=2048,
        top_k=3
    )

    # Connect to Weaviate instance
    client = get_weaviate_client()
    vectorstore = Weaviate(
        client=client,
        index_name="PDFDocuments",  # Class name in Weaviate
        text_key="content",
        attributes=["source", "title"]
    )

    # Create custom prompt
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful AI assistant for the Winback team at 411 Locals. 
Use only the provided context to answer the question. Be specific and back your answers with examples when possible.

Context:
{context}

Question:
{question}
"""
    )

    # Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=gemini,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return qa_chain