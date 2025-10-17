# Healthcare FAQ & Medical Information Assistant 🏥

An intelligent chatbot that combines Retrieval-Augmented Generation (RAG), live web search, and multiple LLM providers to deliver accurate medical information and health advice.

## 🌟 Features

### Core Functionality
- **RAG Integration**: Retrieves relevant information from a curated medical knowledge base using FAISS vector store
- **Live Web Search**: Performs real-time web searches using DuckDuckGo when additional information is needed
- **Multiple Response Modes**: 
  - **Concise Mode**: Quick, summarized answers (max 150 words)
  - **Detailed Mode**: Comprehensive explanations with full context (max 500 words)
- **Document Upload**: Add custom medical documents (PDF/TXT) to enhance the knowledge base
- **Multi-Provider Support**: Compatible with OpenAI, Groq, and Google Gemini LLMs

### Additional Features
- Customizable system prompts
- Chat history export
- Persistent vector store
- Clean, intuitive Streamlit interface
- Error handling and logging

## 🎯 Use Case

This chatbot addresses a common problem: patients and healthcare seekers need quick, accurate information about medical conditions, symptoms, and treatments. Instead of searching through multiple websites, users can ask natural language questions and receive:

- Evidence-based medical information
- Context from trusted knowledge base documents
- Latest information from web searches
- Responses tailored to their preference (concise or detailed)

**Important**: This tool provides general health information for educational purposes only and is NOT a substitute for professional medical advice.

## 🏗️ Architecture

### Technology Stack
- **Framework**: Streamlit
- **LLM Providers**: OpenAI GPT-4, Groq Llama 3.1, Google Gemini
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Web Search**: DuckDuckGo Search API
- **Document Processing**: LangChain

### Project Structure
```
AI_UseCase/
├── config/
│   └── config.py              # API keys and configuration settings
├── models/
│   ├── llm.py                 # LLM model implementations (OpenAI, Groq, Gemini)
│   └── embeddings.py          # HuggingFace embedding model setup
├── utils/
│   ├── rag.py                 # RAG system with FAISS vector store
│   ├── web_search.py          # DuckDuckGo web search functionality
│   └── document_loader.py     # Document processing and chunking
├── data/
│   ├── medical_docs/          # Sample medical documents
│   └── vector_store/          # Persistent FAISS vector store
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- API key from at least one LLM provider (Groq recommended for free tier)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AI_UseCase
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys

You can set API keys as environment variables or directly in `config/config.py`:

**Option A: Environment Variables (Recommended)**
```bash
export GROQ_API_KEY="your-groq-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

**Option B: Update config.py**
Edit `config/config.py` and replace the empty strings with your API keys.

**Get API Keys:**
- **Groq** (Free tier available): https://console.groq.com/keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://aistudio.google.com/app/apikey

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Basic Usage
1. Navigate to the **Chat** page using the sidebar
2. Select your preferred LLM provider
3. Choose response mode (Concise or Detailed)
4. Enable RAG and/or Web Search as needed
5. Start asking questions!

### Example Questions
- "What are the symptoms of the common cold?"
- "How can I prevent diabetes?"
- "What is hypertension and how is it treated?"
- "What should I do if I have a persistent cough?"
- "What are the risk factors for heart disease?"

### Advanced Features

**Custom System Prompts**: Modify the AI's behavior and personality through the sidebar configuration.

**Document Upload**: Add your own medical documents to the knowledge base:
1. Click "Browse files" in the sidebar
2. Select a PDF or TXT file
3. Click "Process Document"
4. The document will be chunked and added to the vector store

**Chat Export**: Save your conversation history by clicking "Export Chat" in the sidebar.

## 🧪 Testing

The application includes built-in error handling and logging. To test:

1. **RAG System**: Ask questions about common cold, diabetes, or hypertension (included in sample documents)
2. **Web Search**: Enable web search and ask about recent medical news or updates
3. **Response Modes**: Toggle between concise and detailed modes to see the difference
4. **Document Upload**: Upload a sample medical document and verify it's added to the knowledge base

## 🔧 Configuration

### Adjusting RAG Parameters
Edit `config/config.py`:
```python
CHUNK_SIZE = 1000          # Size of document chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
TOP_K_RESULTS = 3          # Number of documents to retrieve
```

### Changing Response Length
```python
CONCISE_MAX_TOKENS = 150   # Max words for concise mode
DETAILED_MAX_TOKENS = 500  # Max words for detailed mode
```

### Switching Embedding Models
```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

## 🐛 Troubleshooting

**Issue**: "No API keys configured"
- **Solution**: Ensure at least one API key is set as an environment variable or in config.py

**Issue**: "Failed to initialize embedding model"
- **Solution**: The model will be downloaded on first run. Ensure you have internet connection and sufficient disk space.

**Issue**: "Error loading vector store"
- **Solution**: Delete the `data/vector_store` directory and restart the app to rebuild the index.

**Issue**: Web search not working
- **Solution**: Ensure you have internet connection. DuckDuckGo search doesn't require an API key.

## 📝 Development Approach

### Problem Definition
Identified the need for a centralized, intelligent medical information assistant that can provide quick answers backed by both curated knowledge and real-time web information.

### Solution Design
1. **RAG Implementation**: Used FAISS for efficient similarity search and HuggingFace embeddings for semantic understanding
2. **Web Search Integration**: Added DuckDuckGo as a fallback for current information not in the knowledge base
3. **Response Modes**: Implemented prompt engineering to control response length and detail level
4. **Modular Architecture**: Separated concerns into config, models, and utils for maintainability

### Challenges Faced
1. **Vector Store Persistence**: Solved by implementing save/load functionality for FAISS
2. **Context Window Management**: Balanced between providing enough context and staying within token limits
3. **Multiple LLM Support**: Created a unified interface for different providers with varying APIs
4. **Document Processing**: Handled both PDF and text files with appropriate chunking strategies

## 🚢 Deployment

This application is deployed on Streamlit Cloud. To deploy your own instance:

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your API keys as secrets in the Streamlit Cloud dashboard
5. Deploy!

**Deployment Link**: [Will be added after deployment]

## 📄 License

This project is created for the NeoStats AI Engineer Case Study.

## 🙏 Acknowledgments

- NeoStats for the opportunity and project template
- LangChain for the excellent RAG framework
- Streamlit for the intuitive web framework
- HuggingFace for the embedding models
- All open-source contributors

## 📧 Contact

For questions or feedback about this implementation, please refer to the accompanying presentation deck.

---

**Disclaimer**: This chatbot provides general health information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

