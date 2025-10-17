"""
Healthcare FAQ & Medical Information Assistant
A chatbot with RAG, web search, and multiple response modes
"""
import streamlit as st
import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.llm import get_available_models
from utils.rag import RAGSystem
from utils.web_search import search_and_format
from utils.document_loader import process_uploaded_file
from Config.config import CONCISE_MAX_TOKENS, DETAILED_MAX_TOKENS


def initialize_rag_system():
    """Initialize the RAG system with medical documents"""
    if 'rag_system' not in st.session_state:
        with st.spinner("Initializing knowledge base..."):
            rag_system = RAGSystem()
            
            # Try to load existing vector store
            if not rag_system.load_vector_store():
                # If no saved vector store, initialize from documents
                docs_path = os.path.join(os.path.dirname(__file__), "data/medical_docs")
                if os.path.exists(docs_path):
                    rag_system.initialize_from_directory(docs_path)
                    rag_system.save_vector_store()
            
            st.session_state.rag_system = rag_system


def get_chat_response(chat_model, messages, system_prompt, use_rag=True, use_web_search=False, response_mode="detailed"):
    """
    Get response from the chat model with RAG and web search support
    
    Args:
        chat_model: The LLM model to use
        messages: Chat history
        system_prompt: System prompt for the model
        use_rag: Whether to use RAG for context
        use_web_search: Whether to use web search
        response_mode: "concise" or "detailed"
    """
    try:
        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""
        
        # Build context from RAG
        context = ""
        if use_rag and 'rag_system' in st.session_state:
            rag_system = st.session_state.rag_system
            if rag_system.is_initialized:
                retrieved_docs = rag_system.retrieve_context(last_message)
                if retrieved_docs:
                    context += "\n\n=== Knowledge Base Context ===\n"
                    context += rag_system.format_context(retrieved_docs)
        
        # Add web search results if enabled
        if use_web_search:
            with st.spinner("Searching the web..."):
                search_results = search_and_format(last_message)
                if search_results and "No search results found" not in search_results:
                    context += "\n\n=== Web Search Results ===\n"
                    context += search_results
        
        # Adjust system prompt based on response mode
        mode_instruction = ""
        if response_mode == "concise":
            mode_instruction = f"\n\nIMPORTANT: Provide a CONCISE response (maximum {CONCISE_MAX_TOKENS} words). Be brief and to the point."
        else:
            mode_instruction = f"\n\nIMPORTANT: Provide a DETAILED response (maximum {DETAILED_MAX_TOKENS} words). Include comprehensive explanations and context."
        
        # Prepare messages for the model
        enhanced_system_prompt = system_prompt + mode_instruction
        if context:
            enhanced_system_prompt += f"\n\nUse the following context to answer the user's question:\n{context}"
        
        formatted_messages = [SystemMessage(content=enhanced_system_prompt)]
        
        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"


def instructions_page():
    """Instructions and setup page"""
    st.title("🏥 Healthcare FAQ Assistant")
    st.markdown("### Welcome to your AI-powered medical information assistant!")
    
    st.markdown("""
    ## 📋 About This Application
    
    This intelligent chatbot helps you get quick, accurate information about common medical conditions, 
    symptoms, and general health advice. It combines multiple AI technologies to provide comprehensive answers:
    
    **Key Features:**
    - **RAG (Retrieval-Augmented Generation)**: Retrieves information from a curated medical knowledge base
    - **Live Web Search**: Searches the internet for the latest health information when needed
    - **Multiple Response Modes**: Choose between concise or detailed answers
    - **Document Upload**: Add your own medical documents to the knowledge base
    - **Multiple LLM Providers**: Supports OpenAI, Groq, and Google Gemini
    
    ## 🔧 Setup Instructions
    
    ### 1. Install Dependencies
    
    ```bash
    pip install -r requirements.txt
    ```
    
    ### 2. Configure API Keys
    
    Set your API keys as environment variables or update the `config/config.py` file:
    
    **For Groq (Recommended - Free tier available):**
    ```bash
    export GROQ_API_KEY="your-groq-api-key"
    ```
    Get your key from: [Groq Console](https://console.groq.com/keys)
    
    **For OpenAI:**
    ```bash
    export OPENAI_API_KEY="your-openai-api-key"
    ```
    Get your key from: [OpenAI Platform](https://platform.openai.com/api-keys)
    
    **For Google Gemini:**
    ```bash
    export GOOGLE_API_KEY="your-google-api-key"
    ```
    Get your key from: [Google AI Studio](https://aistudio.google.com/app/apikey)
    
    ### 3. Run the Application
    
    ```bash
    streamlit run app.py
    ```
    
    ## 🎯 How to Use
    
    1. **Navigate to the Chat page** using the sidebar
    2. **Select your preferred LLM provider** (if multiple API keys are configured)
    3. **Choose your response mode**:
       - **Concise**: Quick, summarized answers (great for simple questions)
       - **Detailed**: Comprehensive explanations with full context
    4. **Enable features**:
       - **Use RAG**: Retrieves information from the medical knowledge base
       - **Web Search**: Searches the internet for current information
    5. **Upload documents** (optional): Add your own medical PDFs or text files
    6. **Start chatting**: Ask questions about health conditions, symptoms, treatments, etc.
    
    ## 💡 Example Questions
    
    - "What are the symptoms of the common cold?"
    - "How can I prevent diabetes?"
    - "What is hypertension and how is it treated?"
    - "What should I do if I have a persistent cough?"
    - "What are the risk factors for heart disease?"
    
    ## ⚠️ Important Disclaimer
    
    This chatbot provides general health information for educational purposes only. It is NOT a substitute 
    for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or 
    other qualified health provider with any questions you may have regarding a medical condition.
    
    ## 🛠️ Technical Details
    
    **Architecture:**
    - Frontend: Streamlit
    - LLM Providers: OpenAI GPT-4, Groq Llama, Google Gemini
    - Vector Store: FAISS
    - Embeddings: HuggingFace sentence-transformers
    - Web Search: DuckDuckGo Search API
    - Document Processing: LangChain
    
    **Project Structure:**
    ```
    AI_UseCase/
    ├── config/          # Configuration and API keys
    ├── models/          # LLM and embedding models
    ├── utils/           # RAG, web search, document loading
    ├── data/            # Medical documents and vector store
    └── app.py           # Main application
    ```
    
    ---
    
    Ready to start? Navigate to the **Chat** page using the sidebar! 🚀
    """)


def chat_page():
    """Main chat interface page"""
    st.title("🤖 Healthcare Assistant Chat")
    
    # Initialize RAG system
    initialize_rag_system()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # LLM Provider Selection
        available_models = get_available_models()
        
        if not available_models:
            st.error("⚠️ No API keys configured! Please check the Instructions page.")
            return
        
        provider_name = st.selectbox(
            "Select LLM Provider:",
            options=list(available_models.keys()),
            index=0
        )
        
        # Response Mode
        st.subheader("📝 Response Mode")
        response_mode = st.radio(
            "Choose response style:",
            options=["detailed", "concise"],
            index=0,
            format_func=lambda x: "📚 Detailed" if x == "detailed" else "⚡ Concise"
        )
        
        # Features
        st.subheader("🔧 Features")
        use_rag = st.checkbox("Use RAG (Knowledge Base)", value=True)
        use_web_search = st.checkbox("Enable Web Search", value=False)
        
        # System Prompt
        st.subheader("🎭 System Prompt")
        system_prompt = st.text_area(
            "Customize AI behavior:",
            value="You are a helpful medical information assistant. Provide accurate, evidence-based health information. Always remind users to consult healthcare professionals for medical advice.",
            height=150
        )
        
        # Document Upload
        st.subheader("📄 Upload Documents")
        uploaded_file = st.file_uploader(
            "Add to knowledge base:",
            type=["txt", "pdf"],
            help="Upload medical documents to enhance the knowledge base"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document"):
                try:
                    with st.spinner("Processing document..."):
                        chunks = process_uploaded_file(uploaded_file)
                        st.session_state.rag_system.add_documents(chunks)
                        st.session_state.rag_system.save_vector_store()
                        st.success(f"✅ Added {len(chunks)} chunks to knowledge base!")
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    
    # Get the selected model
    try:
        chat_model = available_models[provider_name]()
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about health conditions, symptoms, or treatments..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chat_response(
                    chat_model, 
                    st.session_state.messages, 
                    system_prompt,
                    use_rag=use_rag,
                    use_web_search=use_web_search,
                    response_mode=response_mode
                )
                st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Healthcare FAQ Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("🏥 Navigation")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )
        
        # Add clear chat button in sidebar for chat page
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            # Export chat history
            if st.button("💾 Export Chat", use_container_width=True):
                if "messages" in st.session_state and st.session_state.messages:
                    chat_text = "\n\n".join([
                        f"{msg['role'].upper()}: {msg['content']}" 
                        for msg in st.session_state.messages
                    ])
                    st.download_button(
                        label="Download Chat History",
                        data=chat_text,
                        file_name="chat_history.txt",
                        mime="text/plain"
                    )
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page()


if __name__ == "__main__":
    main()

