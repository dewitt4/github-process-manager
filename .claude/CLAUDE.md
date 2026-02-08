# GitHub Process Manager - Claude Development Guide

## Project Overview

This is a lightweight, local AI-powered assistant that combines Retrieval-Augmented Generation (RAG) with Google's Gemini API and GitHub repository integration. Built with Python and Flask, it provides a browser-based interface for intelligent document-aware conversations and professional process documentation. Supports multiple use cases: SOX compliance audits, MLOps workflows, DevOps pipelines, and general process documentation.

## Architecture

### Technology Stack
- **Backend**: Python 3.8+ with Flask
- **AI/ML**: Google Gemini API (gemini-2.5-flash, text-embedding-004)
- **Vector Database**: ChromaDB (local persistence)
- **GitHub Integration**: PyGithub
- **Document Processing**: python-docx, PyPDF2
- **Document Generation**: python-docx (Word reports)
- **Frontend**: HTML, CSS, JavaScript (vanilla)

### Core Components

1. **app.py** - Flask application with REST API endpoints
2. **rag_engine.py** - Document processing and vector retrieval using ChromaDB
3. **gemini_client.py** - Gemini API integration with multi-template support
4. **github_client.py** - GitHub API client for repository data and workflow triggers
5. **word_generator.py** - Professional Word document generation (process reports)
6. **config.py** - Centralized configuration and validation
7. **logger.py** - Application logging with rotation

## Key Features

- 📚 **RAG Document Processing**: Upload .txt, .pdf, .docx files for knowledge base
- 🤖 **Gemini AI Integration**: Context-aware responses using Gemini 2.5 Flash
- 🔗 **GitHub Integration**: Access PRs, issues, workflows, and repository files
- ⚡ **GitHub Actions**: Manually trigger workflows from the UI
- 📄 **Word Document Generation**: Create professionally formatted process documentation
- 🎯 **Multi-Template Support**: SOX audits, MLOps workflows, DevOps pipelines, generic docs
- 🎨 **Clean UI**: Light blue/white professional interface ("GitHub Process Manager" branding)
- 🔒 **Secure**: Environment-based configuration with .env

## Use Case Templates

### 1. SOX Audit Reports
**Detection Keywords**: sox, control, audit, compliance, internal control

**5-Section Structure**:
1. Control Objective
2. Risks Addressed
3. Testing Procedures
4. Test Results and Findings
5. Conclusion and Recommendation

### 2. MLOps Workflow Documentation
**Detection Keywords**: model, mlops, machine learning, training, inference, dataset

**5-Section Structure**:
1. Model Overview
2. Data Pipeline
3. Training Process
4. Validation Results
5. Deployment Plan

### 3. DevOps Pipeline Documentation
**Detection Keywords**: pipeline, ci/cd, deployment, build, release, kubernetes, docker

**5-Section Structure**:
1. Pipeline Overview
2. Build Steps
3. Test and Quality Gates
4. Deployment Process
5. Monitoring and Rollback

### 4. Generic Process Documentation
**Fallback**: Used when no specific keywords detected

**5-Section Structure**:
1. Overview
2. Key Components
3. Procedures
4. Analysis Results
5. Conclusion and Recommendations

## Development Notes

### Environment Setup
```bash
# Virtual environment is at .venv (not venv)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configuration
# Copy .env.template to .env and add:
# - GEMINI_API_KEY (required)
# - GITHUB_TOKEN (optional)
# - GITHUB_REPO_URL (optional)
```

### Running the Application
```bash
# Quick start (automated)
.\start.ps1

# Manual start
python app.py
# Access at http://localhost:5000
```

### Project Structure
```
github-process-manager/
├── .venv/                  # Virtual environment
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── logger.py               # Logging setup
├── rag_engine.py           # RAG/ChromaDB engine
├── gemini_client.py        # Gemini API client with template detection
├── github_client.py        # GitHub API client
├── word_generator.py       # Word document generation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.template           # Template for .env
├── start.ps1               # PowerShell startup script
├── start.bat               # Batch launcher
├── templates/              # Jinja2 templates
│   ├── base.html           # Base template ("GitHub Process Manager" header)
│   ├── index.html          # Chat interface
│   └── settings.html       # Settings & GitHub Actions
├── static/
│   └── css/
│       └── style.css       # Application styling (#4A90E2 brand color)
├── .github/
│   └── workflows/
│       ├── process-analysis-doc.yml  # Generic process workflow
│       └── sox-analysis-doc.yml      # Legacy SOX workflow
├── chroma_db/              # ChromaDB storage (auto-created)
├── uploads/                # Temporary uploads (auto-created)
├── generated_reports/      # Word documents (auto-created)
└── app.log                 # Application logs
```

## API Endpoints

### Chat
- `POST /api/chat` - Send query, get AI response with RAG context

### Document Management
- `POST /api/upload` - Upload document for RAG processing
- `GET /api/rag/stats` - Get RAG database statistics
- `POST /api/rag/clear` - Clear all RAG documents

### GitHub Integration
- `POST /api/github/connect` - Connect to repository
- `GET /api/github/info` - Get repository metadata
- `GET /api/github/workflows` - List available workflows
- `POST /api/github/workflow/trigger` - Trigger workflow manually
- `POST /api/github/process-analysis/trigger` - Trigger process analysis workflow
- `GET /api/github/artifacts/check/<run_id>` - Check and download workflow artifacts
- `GET /api/github/pulls` - Get pull requests
- `GET /api/github/issues` - Get issues

### Word Document Generation
- `POST /api/generate-word-report` - Generate Word document from analysis
- `GET /api/download/<filename>` - Download generated Word document
- `GET /api/reports/list` - List all generated reports
- `POST /api/reports/cleanup` - Delete old reports (24h+)

### System
- `GET /health` - Health check and system status

## Configuration Options

Key settings in `config.py`:
- `CHUNK_SIZE`: 800 characters per document chunk
- `CHUNK_OVERLAP`: 200 characters overlap between chunks
- `TOP_K_RESULTS`: 3 RAG chunks retrieved per query
- `GEMINI_MODEL`: gemini-2.5-flash
- `GEMINI_EMBEDDING_MODEL`: text-embedding-004
- `TEMPERATURE`: 0.7
- `MAX_OUTPUT_TOKENS`: 2048

## Query Type Detection

The system automatically detects query type and applies appropriate structured response format:

**Detection Process** (`gemini_client.py:_detect_query_type()`):
1. Analyze user query for keywords
2. Match to template type: `sox_audit`, `mlops_workflow`, `devops_pipeline`, or `generic`
3. Apply corresponding prompt template with 5-section structure
4. Frontend detects structured response for Word download option

## Word Document Generation

### Process Flow
1. **Detection**: Frontend JavaScript detects structured responses (5-section format)
2. **User Action**: "📄 Download Word Report" button appears
3. **API Call**: `POST /api/generate-word-report` with analysis text
4. **Document Creation**: `word_generator.py:create_process_document()`
   - Parse 5 sections from response text
   - Apply professional formatting (Calibri, proper spacing)
   - Add header: "GitHub Process Manager | Process Documentation"
   - Use brand color: `#4A90E2` (RGB 74, 144, 226)
   - Generate metadata table (timestamp, query, report type)
   - Add page footer with page numbers
5. **Storage**: Save to `generated_reports/Process_Analysis_<name>_<timestamp>.docx`
6. **Download**: Return download URL to user

### Functions

**`create_process_document(analysis_text, process_name, metadata)`**
- Primary function for document generation
- Generic naming for all use cases
- Returns filename

**`create_sox_word_document()` [Legacy]**
- Backward compatibility wrapper
- Calls `create_process_document()` with renamed parameters

**`list_generated_reports()`**
- Lists all .docx files in `generated_reports/`
- Returns file metadata (size, created, modified)

**`cleanup_old_reports(hours=24)`**
- Deletes reports older than specified hours
- Default: 24 hours retention

### Styling & Branding

**Header**: "GitHub Process Manager | Process Documentation"  
**Title Color**: Professional Blue (#4A90E2)  
**Section Headings**: Large, colored, bold  
**Font**: Calibri 11pt (body), Pt 14-18 (headings)  
**Footer**: Page numbers + "Confidential"

**Legacy (Removed)**:
- ❌ "KPMG | SOX Control Testing"
- ❌ KPMG Blue (#00338D / RGB 0, 51, 141)

## RAG Processing Flow

1. **Document Upload** → Extract text (.txt, .pdf, .docx)
2. **Chunking** → Split into 800-char chunks with 200-char overlap
3. **Embedding** → Generate vectors using Gemini Embedding API
4. **Storage** → Store in ChromaDB with metadata
5. **Retrieval** → Query ChromaDB for top-K relevant chunks
6. **Response** → Combine RAG context + GitHub data + user query → Gemini

## GitHub Integration

### Supported Operations
- Repository metadata (stars, forks, language)
- Pull requests (list, search, filter by state)
- Issues (list, search, filter by state)
- Workflow runs (status, conclusion)
- Repository files (browse, read)
- Manual workflow triggers (via `create_workflow_dispatch`)
- Artifact download from workflow runs
- Process analysis report generation via GitHub Actions

### GitHub Actions Workflows

**process-analysis-doc.yml** (Primary)
- Generic process documentation workflow
- Inputs: `process_name`, `process_data`, `analysis_type`
- Generates Word document with "GitHub Process Manager" branding
- Professional blue color scheme (#4A90E2)
- Artifact name: `process-report`

**sox-analysis-doc.yml** (Legacy)
- Backward compatibility for SOX-specific workflows
- Same functionality, legacy naming conventions
- Artifact name: `sox-report`

### Required Permissions
GitHub token needs:
- `repo` - Full repository access
- `workflow` - Trigger GitHub Actions

## Common Development Tasks

### Adding a New Template Type
1. Add keywords to `gemini_client.py:_detect_query_type()`
2. Create prompt template function (e.g., `_get_mlops_instructions()`)
3. Update frontend detection in `templates/index.html`
4. Test with sample queries

### Adding a New Route
1. Define route handler in `app.py`
2. Add error handling with try/except
3. Log operations using `logger.info()` / `logger.error()`
4. Return JSON responses

### Modifying RAG Behavior
- Edit `rag_engine.py`
- Adjust `CHUNK_SIZE`, `CHUNK_OVERLAP` in `config.py`
- Change `TOP_K_RESULTS` for more/fewer context chunks

### Updating UI
- Templates: `templates/*.html`
- Styles: `static/css/style.css`
- Theme colors in CSS `:root` variables
- Brand color: `#4A90E2` (professional blue)
- Project name: "GitHub Process Manager"

### Adding Document Formats
1. Add extension to `ALLOWED_EXTENSIONS` in `config.py`
2. Implement text extraction in `rag_engine.py:extract_text()`
3. Install any required libraries

## Backward Compatibility

The rebranding from "Local AI RAG Chatbot" to "GitHub Process Manager" maintains full backward compatibility:

### Legacy Function Support

**word_generator.py**
- `create_sox_word_document()` → Wrapper for `create_process_document()`
- Parameters: `control_name` automatically mapped to `process_name`
- Existing integrations continue to work without code changes

**github_client.py**
- `trigger_sox_workflow()` → Wrapper for `trigger_process_workflow()`
- Legacy workflow `sox-analysis-doc.yml` still exists and functional
- New workflow `process-analysis-doc.yml` uses generic naming

**API Endpoints**
- `/api/github/sox-analysis/trigger` → Redirects to `/api/github/process-analysis/trigger`
- Both endpoints accept same parameters
- Frontend updated to use new endpoint

### Migration Path

**For Existing Code**:
1. Old function names continue to work (wrappers in place)
2. Gradually update to new naming conventions
3. Test with both old and new endpoints
4. Switch to new generic naming when ready

**For GitHub Actions**:
1. Both workflows co-exist: `process-analysis-doc.yml` (new) and `sox-analysis-doc.yml` (legacy)
2. Artifact names: `process-report` (new) vs `sox-report` (legacy)
3. Same functionality, different branding
4. Choose workflow based on preference

## Troubleshooting

### Common Issues

**"GEMINI_API_KEY is not set"**
- Create `.env` from `.env.template`
- Add valid Gemini API key

**ChromaDB errors**
- Delete `chroma_db/` directory
- Restart application

**GitHub connection fails**
- Verify token has `repo` and `workflow` scopes
- Check repository URL format
- Ensure token hasn't expired

**Import errors**
- Activate virtual environment: `.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### Logs
Check `app.log` for detailed error messages and stack traces.

## Performance Considerations

- **Lightweight Design**: No GPU required, runs on CPU
- **ChromaDB**: Local vector database, no external service needed
- **Chunking Strategy**: Efficient 800-char chunks balance context and speed
- **Caching**: ChromaDB automatically caches embeddings
- **Resource Usage**: ~200-500MB RAM typical usage

## Security Notes

- `.env` file is gitignored - never commit API keys
- Session secrets managed via `FLASK_SECRET_KEY`
- File uploads limited to 16MB
- Allowed file extensions whitelist (.txt, .pdf, .docx)
- GitHub token permissions should be minimal (repo + workflow only)

## Future Enhancements (Ideas)

- [ ] Session-based chat history
- [ ] Export conversations to PDF
- [ ] Markdown rendering in chat responses
- [ ] Multiple RAG collections (project-based)
- [ ] Real-time GitHub webhook integration
- [ ] Docker containerization
- [ ] Authentication/multi-user support
- [ ] Streaming responses from Gemini
- [ ] Code syntax highlighting in responses
- [x] Multi-template support (SOX, MLOps, DevOps, Generic)
- [x] Word document generation
- [x] GitHub Actions workflow triggers
- [ ] Custom template editor in UI
- [ ] Template configuration via JSON files
- [ ] Logo upload and customization
- [ ] Company branding configuration

## Links & Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: February 7, 2026  
**Python Version**: 3.8+  
**Status**: ✅ Fully Production Ready  
**Project**: GitHub Process Manager (formerly "Local AI RAG Chatbot")