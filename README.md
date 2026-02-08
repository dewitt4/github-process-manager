# 🤖 GitHub Process Manager - AI-Powered Documentation Assistant

A lightweight, local AI-powered assistant that combines **Retrieval-Augmented Generation (RAG)** with the **Gemini API** and **GitHub repository integration**. Upload reference documents, connect to your GitHub repositories, and get intelligent responses for process documentation, SOX compliance, MLOps workflows, DevOps pipelines, and more.

## ✨ Features

- 🧠 **RAG-Powered Responses**: Upload documents (.txt, .pdf, .docx) to create a knowledge base
- 🤖 **Gemini AI Integration**: Leverages Google's Gemini Pro for intelligent responses
- 🔗 **GitHub Repository Connection**: Access PRs, issues, workflow runs, and repository files
- ⚡ **GitHub Actions Control**: Manually trigger workflows directly from the interface
- � **Word Document Generation**: Create professionally formatted process documentation
- 💻 **Browser-Based UI**: Clean, professional interface with light blue and white theme
- 🪶 **Lightweight & Local**: Runs entirely on your machine with minimal resource usage
- 📊 **ChromaDB Vector Storage**: Efficient document embedding and retrieval
- 🔒 **Secure Configuration**: Environment-based secrets management
- 🎯 **Multi-Template Support**: SOX audits, MLOps workflows, DevOps pipelines, and generic documentation

## 🎯 Use Cases

### SOX Compliance & Auditing
- Document internal controls and procedures
- Generate 5-section SOX control analysis reports
- Track testing procedures and results
- Create audit-ready Word documents

### MLOps Workflows
- Document machine learning pipelines
- Track model training and validation
- Generate deployment documentation
- Monitor ML workflow processes

### DevOps Pipelines
- Document CI/CD pipelines
- Track build and deployment processes
- Generate pipeline documentation
- Monitor infrastructure changes

### General Process Documentation
- Create structured process documentation
- Generate professional Word reports
- Track project workflows
- Document best practices and procedures

## 📋 Prerequisites

- **Python 3.8+**
- **Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **GitHub Personal Access Token** (optional, for GitHub features)
- **Git** (for cloning the repository)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd github-process-manager
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the template and edit with your credentials:

```bash
# Windows
copy .env.template .env

# macOS/Linux
cp .env.template .env
```

Edit `.env` file:

```env
# Required: Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: GitHub Integration
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_REPO_URL=https://github.com/username/repository

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

**Getting Your API Keys:**

- **Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **GitHub Token**: Go to GitHub Settings → Developer Settings → Personal Access Tokens → Generate new token
  - Required scopes: `repo`, `workflow` (for triggering actions)

### 5. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## � Docker Deployment (Recommended)

For a consistent, isolated environment, use Docker:

### Quick Start with Docker Compose

```bash
# 1. Configure environment
cp .env.template .env
# Edit .env with your API keys

# 2. Start the application
docker-compose up -d

# 3. View logs
docker-compose logs -f app

# 4. Access at http://localhost:5000
```

### Development with VS Code Dev Container

1. Install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
2. Open project in VS Code
3. Press `F1` → "Remote-Containers: Reopen in Container"
4. Environment is automatically configured with all dependencies

### Docker Commands

```bash
# Stop the application
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Production mode
docker-compose -f docker-compose.prod.yml up -d

# View container shell
docker-compose exec app /bin/bash
```

**For detailed Docker setup**, see [README.docker.md](README.docker.md)

## �📖 Usage Guide

### Upload Reference Documents

1. Navigate to the main **Chat** page
2. Click **"Choose File"** in the upload section
3. Select a document (.txt, .pdf, or .docx)
4. Click **"Upload"** to process the document
5. The document will be chunked, embedded, and stored in ChromaDB

### Connect to GitHub Repository

1. Go to the **Settings** page
2. Enter your GitHub repository URL (e.g., `https://github.com/username/repo`)
3. Click **"Connect Repository"**
4. Once connected, the chatbot can access PRs, issues, and workflows

### Chat with the AI

1. Type your question in the chat input
2. The chatbot will:
   - Retrieve relevant document chunks from your uploaded files
   - Fetch related GitHub repository data (if connected)
   - Generate a response using Gemini AI with all context
3. Responses cite sources from documents and GitHub data

### Trigger GitHub Actions

1. Go to **Settings** → **GitHub Actions**
2. Click **"Load Workflows"**
3. Click **"Trigger"** on any workflow to manually start it

## 🏗️ Project Structure

```
github-process-manager/
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── logger.py               # Logging setup
├── rag_engine.py           # RAG document processing
├── gemini_client.py        # Gemini API integration
├── github_client.py        # GitHub API integration
├── word_generator.py       # Word document generation
├── requirements.txt        # Python dependencies
├── .env.template           # Environment variable template
├── .gitignore             # Git ignore rules
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Chat interface
│   └── settings.html      # Settings page
├── static/
│   └── css/
│       └── style.css      # Application styling
├── .github/
│   └── workflows/
│       ├── process-analysis-doc.yml  # Generic process workflow
│       └── sox-analysis-doc.yml      # SOX-specific workflow (legacy)
├── chroma_db/             # ChromaDB storage (auto-created)
├── uploads/               # Temporary upload folder (auto-created)
├── generated_reports/     # Generated Word documents (auto-created)
└── README.md              # This file
```

## 🔧 Configuration Options

Edit `config.py` or set environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | **Required** |
| `GITHUB_TOKEN` | GitHub personal access token | Optional |
| `GITHUB_REPO_URL` | GitHub repository URL | Optional |
| `FLASK_SECRET_KEY` | Flask session secret | Auto-generated |
| `CHROMA_DB_PATH` | ChromaDB storage location | `./chroma_db` |
| `CHUNK_SIZE` | Characters per document chunk | 800 |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 |
| `TOP_K_RESULTS` | RAG chunks to retrieve | 3 |

## 🛠️ API Endpoints

### Chat
- `POST /api/chat` - Send query and get AI response

### Document Management
- `POST /api/upload` - Upload document for RAG
- `GET /api/rag/stats` - Get RAG database statistics
- `POST /api/rag/clear` - Clear all documents

### GitHub Integration
- `POST /api/github/connect` - Connect to repository
- `GET /api/github/info` - Get repository info
- `GET /api/github/workflows` - List workflows
- `POST /api/github/workflow/trigger` - Trigger workflow
- `GET /api/github/pulls` - Get pull requests
- `GET /api/github/issues` - Get issues

### System
- `GET /health` - Health check endpoint

## ❗ Troubleshooting

### "Configuration validation failed: GEMINI_API_KEY is not set"
- Make sure you've created a `.env` file from `.env.template`
- Add your Gemini API key to the `.env` file
- Restart the application

### Documents not being processed
- Check file format (.txt, .pdf, .docx only)
- Ensure file size is under 16MB
- Check `app.log` for detailed error messages

### GitHub connection failing
- Verify your GitHub token has correct permissions (`repo`, `workflow`)
- Check that the repository URL is correct
- Ensure the token hasn't expired

### ChromaDB errors
- Delete the `chroma_db/` folder and restart the application
- This will clear all uploaded documents

## 📝 Features in Detail

### RAG (Retrieval-Augmented Generation)
- Automatically chunks documents into manageable pieces
- Generates embeddings using Gemini Embedding API
- Stores vectors in ChromaDB for fast similarity search
- Retrieves top-K most relevant chunks for each query

### Gemini Integration
- Uses Gemini Pro for natural language understanding
- Combines RAG context with GitHub data in prompts
- Configurable temperature and token limits
- Robust error handling and retries

### GitHub Features
- Read repository metadata
- List and search pull requests and issues
- Access workflow run history
- Trigger workflows with custom inputs
- Retrieve repository files and structure

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- **Google Gemini API** for AI capabilities
- **ChromaDB** for vector storage
- **PyGithub** for GitHub integration
- **Flask** for the web framework

## 📧 Support

For issues or questions, please check the logs in `app.log` or review the troubleshooting section above.

---

**Built with ❤️ using Python, Flask, and ChromaDB**