import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import tempfile

st.set_page_config(page_title='Document QA ChatBot', page_icon='🤖', layout='centered')

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")

prompt = ChatPromptTemplate.from_template("""
Answer the questions based on the provided text only.
If answer cannot find from the context, please reply that the information is not found in the provided documents.

<context>
{context}
</context>
Questions:{input}
""")

# ========== IMPORTANT: Initialize session state at the very beginning ==========
if 'vectors' not in st.session_state:
    st.session_state.vectors = None
if 'embedding_model' not in st.session_state:
    st.session_state.embedding_model = None
if 'text_splitter' not in st.session_state:
    st.session_state.text_splitter = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title('📚 Document QA ChatBot')

# Sidebar
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            # Initialize models only once
            if st.session_state.embedding_model is None:
                st.session_state.embedding_model = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
            
            if st.session_state.text_splitter is None:
                st.session_state.text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=5000, 
                    chunk_overlap=200
                )
            
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            # Load and process PDF
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            chunks = st.session_state.text_splitter.split_documents(docs)
            
            # Create vector store
            st.session_state.vectors = FAISS.from_documents(
                chunks, 
                st.session_state.embedding_model
            )
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            st.success(f"✅ Ready! {len(chunks)} chunks created. You can now ask questions.")
    
    if st.button("🗑️ Clear & Reset"):
        st.session_state.vectors = None
        st.session_state.chat_history = []
        st.rerun()

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt1 := st.chat_input("Ask a question about your document:"):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt1})
    with st.chat_message("user"):
        st.write(prompt1)
    
    # Get response
    with st.chat_message("assistant"):
        if st.session_state.vectors is not None:
            try:
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 3})
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                response = retrieval_chain.invoke({"input": prompt1})
                answer = response["answer"]
                st.write(answer)
                # Save to history
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.write(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        else:
            msg = "⚠️ Please upload a PDF document first using the sidebar."
            st.write(msg)
            st.session_state.chat_history.append({"role": "assistant", "content": msg})