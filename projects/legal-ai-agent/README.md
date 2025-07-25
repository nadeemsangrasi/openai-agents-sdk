# Advance Legal AI Agent with Advance memory management 🤖⚖️

A next-generation legal AI assistant leveraging advanced memory frameworks, LLMs, and modern cloud technologies to deliver accurate, contextual, and secure legal support.

---

## �� Key Features

- **Advanced Memory Management:** Combines short-term memory (thread-based, for immediate conversational context) with long-term memory (powered by LangGraph & LangMem, including semantic, episodic, and procedural memory) for robust, context-aware legal assistance.

- **Tri-Memory Architecture (Powered by LangGraph & LangMem)**

  - 🧠 **Semantic Memory:** Stores legal definitions, statutes, and precedents for instant retrieval.
  - 📝 **Episodic Memory:** Remembers case-specific details and user interactions for personalized assistance.
  - ⚙️ **Procedural Memory:** Documents legal workflows and processes for step-by-step guidance.

- **Intelligent Interaction**

  - Context-aware, professional legal responses
  - Automatic conversation summarization
  - Persistent, multi-user memory across sessions

- **Security & Authentication**

  - OAuth2 (Google & GitHub) for secure login
  - User-specific, isolated memory spaces
  - Secure data persistence with PostgreSQL
  - Sanitized username handling

- **Agent Tools**

  - Semantic memory operations (search, retrieval, update)
  - Episodic memory tracking for ongoing cases
  - Procedural memory management for legal processes

- **Developer Friendly**
  - Modular, extensible codebase
  - Easy-to-add tools and memory modules
  - Comprehensive test and config structure

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Chainlit** (chat interface)
- **LangChain** (LLM orchestration)
- **LangGraph** & **LangMem** (advanced memory management)
- **OpenAI Agents** (agent framework)
- **Google Gemini API** (LLM & embeddings)
- **PostgreSQL** (persistent storage)
- **Pydantic** (data validation)
- **psycopg2** (PostgreSQL adapter)
- **python-dotenv** (environment management)
- **pypdf2**, **python-docx** (document parsing)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Google API access
- OAuth credentials

### Environment Setup

Create a `.env` file with your credentials:

```env
GEMINI_API_KEY="your-gemini-api-key"
MODEL_NAME="gemini-2.0-flash"
BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
EMBEDDING_MODEL="models/text-embedding-004"
PG_URL="your-postgresql-connection-string"

# OAuth Configuration
OAUTH_GOOGLE_CLIENT_ID="your-google-client-id"
OAUTH_GOOGLE_CLIENT_SECRET="your-google-client-secret"
CHAINLIT_AUTH_SECRET="your-chainlit-secret"
```

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd legal-ai-agent
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏗️ Project Structure

```
legal-ai-agent/
├── src/
│   ├── legal_ai_agent/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── config/
│   ├── models/
│   ├── prompts/
│   ├── tools/
│   └── utils/
├── tests/
├── .env
├── README.md
└── pyproject.toml
```

---

## 💻 Usage

1. Start the application:
   ```bash
   uv run agent
   ```
2. Access the web interface at [http://localhost:8000](http://localhost:8000)
3. Authenticate using OAuth
4. Use the agent for:
   - Legal definitions & research
   - Contract review & analysis
   - Case precedent lookup
   - Legal process guidance

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT capabilities
- Google for Gemini API
- Chainlit for chat interface
- LangGraph & LangMem for advanced memory management
- PostgreSQL for data persistence

---

## 📞 Support

- Open an issue in the repository
- Contact the maintainers
- Check documentation

---

Built with ❤️ for the legal community
