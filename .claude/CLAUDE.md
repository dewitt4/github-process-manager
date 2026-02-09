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
- **Containerization**: Docker, Docker Compose, VS Code Dev Containers

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

**Option 1: Docker (Recommended)**
```bash
# Copy environment template
cp .env.template .env
# Edit .env with your API keys

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Access at http://localhost:5000

# Stop
docker-compose down
```

**Option 2: VS Code Dev Container**
1. Install "Remote - Containers" extension
2. Press F1 → "Remote-Containers: Reopen in Container"
3. Environment automatically configured

**Option 3: Local Python (Manual)**
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
├── document_templates.json # Document template configuration (Phase 3)
├── start.ps1               # PowerShell startup script
├── start.bat               # Batch launcher
├── Dockerfile              # Docker container definition
├── .dockerignore           # Docker build exclusions
├── docker-compose.yml      # Development Docker setup
├── docker-compose.prod.yml # Production Docker setup
├── Makefile                # Docker convenience commands
├── README.docker.md        # Docker documentation
├── .devcontainer/
│   └── devcontainer.json   # VS Code Remote Containers config
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
- `TEMPERATURE`: 0.7 (configurable via `GEMINI_TEMPERATURE`)
- `MAX_OUTPUT_TOKENS`: 2048 (configurable via `GEMINI_MAX_TOKENS`)

## AI System Prompt Customization

### Overview

The application supports flexible system prompt configuration through three mechanisms:
1. **Pre-defined Templates** - 6 ready-to-use prompt personas
2. **Custom Prompts** - Write your own system instructions
3. **Multi-level Configuration** - Environment variables + Session-based UI changes

### Pre-defined Templates

Located in `config.py:SYSTEM_PROMPTS` dictionary:

**1. default**
- Balanced, helpful assistant for general queries
- Professional and concise responses
- Suitable for most use cases

**2. technical_expert**
- Deep technical explanations with implementation details
- Code examples and best practices
- Architecture diagrams and design patterns
- Ideal for: Software engineering, system design, debugging

**3. security_auditor**
- Security-focused analysis and threat modeling
- Compliance framework expertise (SOX, GDPR, ISO 27001)
- Risk assessment and remediation recommendations
- Ideal for: Security audits, compliance documentation, vulnerability analysis

**4. developer_assistant**
- Code-heavy responses with working examples
- Multiple programming languages and frameworks
- Debugging, optimization, and refactoring suggestions
- Ideal for: Active development, code reviews, troubleshooting

**5. data_analyst**
- Structured analysis with metrics and KPIs
- Data visualization recommendations
- Statistical insights and trend analysis
- Ideal for: Reports, dashboards, business intelligence

**6. technical_educator**
- Clear, beginner-friendly explanations
- Analogies and real-world examples
- Step-by-step learning paths
- Ideal for: Training, documentation, onboarding

### Configuration Methods

#### Method 1: Environment Variables (.env)

**Permanent configuration** (persists across server restarts):

```env
# Option A: Use a pre-defined template
SYSTEM_PROMPT_TEMPLATE=technical_expert

# Option B: Set a custom prompt
CUSTOM_SYSTEM_PROMPT="You are a cloud infrastructure expert specializing in AWS. Provide detailed, actionable recommendations."
```

**Priority**: `CUSTOM_SYSTEM_PROMPT` > `SYSTEM_PROMPT_TEMPLATE` > default template

#### Method 2: Settings UI (Session-based)

**Temporary configuration** (session-based, resets on server restart):

1. Navigate to `/settings`
2. Scroll to "AI System Prompt Configuration"
3. Select template or create custom prompt
4. Click "Update Prompt"
5. Changes apply immediately to new chat queries

**Implementation**:
- Frontend: `templates/settings.html` (lines added for prompt UI)
- JavaScript: Event handlers for template selection, custom editor, save/reset
- API Integration: `/api/prompts/update`, `/api/prompts/reset`

#### Method 3: API Endpoints (Programmatic)

**For automation and integration**:

```python
# Get available templates
GET /api/prompts/templates
# Response: {"templates": {...}, "current_template": "default"}

# Get current prompt
GET /api/prompts/current
# Response: {"prompt": "...", "source": "template", "template": "default"}

# Update with template
POST /api/prompts/update
# Body: {"template": "technical_expert"}

# Update with custom prompt
POST /api/prompts/update
# Body: {"custom_prompt": "Your custom instruction..."}

# Reset to default
POST /api/prompts/reset
# Response: {"message": "Prompt reset to default"}
```

### Implementation Details

**config.py**
- `SYSTEM_PROMPTS`: Dictionary of all 6 templates
- `get_system_prompt()`: Returns active prompt (checks `CUSTOM_SYSTEM_PROMPT` → `SYSTEM_PROMPT_TEMPLATE` → default)
- `get_available_prompts()`: Returns list of template names

**gemini_client.py**
- `_build_prompt()`: Calls `Config.get_system_prompt()` for each query
- Dynamic prompt injection before RAG context and user query

**app.py**
- Session variable: `session.get('custom_system_prompt')` for UI-based changes
- 5 new API endpoints for prompt management
- Re-initialization of `GeminiClient` on prompt updates

**templates/settings.html**
- Dropdown: 7 options (6 templates + custom)
- Custom editor: Textarea with live preview
- JavaScript: Async fetch calls to API endpoints
- Status feedback: Success/error messages

### Usage Examples

**Example 1: Security Audit Mode**
```env
SYSTEM_PROMPT_TEMPLATE=security_auditor
```
Result: All responses focus on security implications, compliance requirements, and risk mitigation.

**Example 2: Custom Corporate Assistant**
```env
CUSTOM_SYSTEM_PROMPT="You are the AI assistant for Acme Corp. Focus on our internal processes, AWS infrastructure, and Python microservices architecture. Reference our coding standards and security policies."
```
Result: Responses tailored to company-specific context.

**Example 3: Session-based Switching**
1. Start with default template
2. User opens Settings → selects "Developer Assistant"
3. Next queries get code-heavy, implementation-focused responses
4. User resets to default before closing
5. Server restart → reverts to `.env` configuration

### Testing the Feature

**Test Template Switching**:
1. Ask: "Explain how authentication works"
2. Switch to `security_auditor` template
3. Ask same question
4. Compare responses (should see security-focused analysis)

**Test Custom Prompt**:
1. Create custom prompt: "You are a DevOps expert. Always mention Docker and Kubernetes."
2. Ask: "How do I deploy this application?"
3. Verify response includes containerization recommendations

**Test Persistence**:
1. Set template via UI
2. Restart server
3. Verify reset to `.env` configuration

### Best Practices

**When to Use Each Template**:
- `default`: General chatbot, mixed queries
- `technical_expert`: Architecture discussions, system design
- `security_auditor`: SOX reports, security reviews, compliance docs
- `developer_assistant`: Active coding sessions, debugging
- `data_analyst`: Business reports, metrics analysis
- `technical_educator`: Training materials, documentation

**Writing Custom Prompts**:
- Be specific about domain expertise
- Include output format preferences
- Mention key technologies or frameworks
- Set tone and style expectations
- Keep under 500 words for best results

**Configuration Strategy**:
- `.env` for default organizational behavior
- UI for temporary context switching
- API for automated workflows or integrations

## Document Template System (Phase 3)

### Overview

The application features a flexible, configurable document template system that allows customization of Word document generation through JSON configuration files and environment variables. This enables users to:
- Customize branding (colors, logos, company names)
- Define custom document structures
- Support multiple document types (SOX audits, MLOps, DevOps, generic)
- Add new templates without code changes

### Configuration Variables

Located in `config.py` (lines 54-60):

**Environment Variables**:
- `PROJECT_NAME` (default: "GitHub Process Manager") - Displayed in document headers
- `COMPANY_NAME` (optional) - Added to header if provided: "Company | Project | Process Documentation"
- `BRAND_COLOR` (default: "#4A90E2") - Hex color for headings and styling
- `DOCUMENT_LOGO_PATH` (optional) - Path to logo image (.png, .jpg, .jpeg, .gif, .bmp)
- `DEFAULT_TEMPLATE_TYPE` (default: "generic") - Default template selection
- `DOCUMENT_TEMPLATES_PATH` (default: "document_templates.json") - Path to template configuration

### Validation Functions

**`validate_color_format(color_string)`** (config.py:110-116)
- Validates hex color format (#RRGGBB)
- Returns True for valid colors or empty strings
- Uses regex pattern: `^#[0-9A-Fa-f]{6}$`

**`validate_logo_path(logo_path)`** (config.py:118-131)
- Checks if logo file exists
- Validates image format (.png, .jpg, .jpeg, .gif, .bmp)
- Returns True for valid paths or empty strings
- Logs warnings for invalid paths

**`get_brand_color_rgb()`** (config.py:180-183)
- Converts hex color to RGB tuple for python-docx
- Returns tuple: (R, G, B) for use with `RGBColor(*brand_rgb)`
- Example: "#4A90E2" → (74, 144, 226)

### Template Configuration File

**document_templates.json** - JSON structure defining all document templates:

```json
{
  "templates": {
    "template_key": {
      "name": "Template Display Name",
      "description": "Template purpose",
      "report_title": "Document Title",
      "sections": [
        {
          "number": 1,
          "title": "Section Title",
          "key": "Section Key",
          "description": "Section purpose"
        }
      ],
      "keywords": ["keyword1", "keyword2"]
    }
  },
  "default_template": "generic",
  "version": "1.0"
}
```

**Built-in Templates**:

1. **sox_audit** - SOX Compliance & Internal Control Testing
   - Sections: Control Objective, Risks Addressed, Testing Procedures, Test Results and Findings, Conclusion and Recommendation
   - Keywords: sox, control, audit, compliance, internal control
   
2. **mlops_workflow** - Machine Learning Operations
   - Sections: Model Overview, Data Pipeline, Training Process, Validation Results, Deployment Plan
   - Keywords: model, mlops, machine learning, training, inference, dataset
   
3. **devops_pipeline** - CI/CD Pipeline Documentation
   - Sections: Pipeline Overview, Build Steps, Test and Quality Gates, Deployment Process, Monitoring and Rollback
   - Keywords: pipeline, ci/cd, cicd, deployment, build, release, kubernetes, docker
   
4. **generic** - General Purpose Documentation
   - Sections: Overview, Key Components, Procedures, Analysis Results, Conclusion and Recommendations
   - Keywords: (none - used as fallback)

### word_generator.py Implementation

**Template Loading** (lines 13-50):
- `load_templates()` function loads JSON on module initialization
- Global `DOCUMENT_TEMPLATES` dictionary stores all templates
- Falls back to built-in generic template if file not found
- Logs number of templates loaded

**Section Parsing** (lines 52-90):
- `parse_analysis_sections(analysis_text, template_type)` - Dynamic section extraction
- Uses template configuration to build regex patterns
- Matches numbered sections (e.g., "1. Control Objective:")
- Returns dict with section keys and extracted content
- Falls back to full text in first section if parsing fails

**Document Generation** (lines 92-230):
- `create_process_document(analysis_text, process_name, metadata, template_type)`
- Template type parameter (defaults to `Config.DEFAULT_TEMPLATE_TYPE`)
- Retrieves template from `DOCUMENT_TEMPLATES` dictionary
- Applies branding from Config: `PROJECT_NAME`, `COMPANY_NAME`, `get_brand_color_rgb()`
- Inserts logo from `DOCUMENT_LOGO_PATH` if configured
- Generates sections dynamically from template configuration
- Professional formatting: Calibri 11pt, colored headings, page numbers

**Backward Compatibility** (lines 290-300):
- `create_sox_word_document()` wrapper for legacy code
- Calls `create_process_document()` with `template_type='sox_audit'`
- Maintains compatibility with existing SOX-focused workflows

### Usage Examples

**Example 1: Custom Company Branding**
```env
PROJECT_NAME=Process Manager
COMPANY_NAME=Acme Corporation
BRAND_COLOR=#FF6600
DOCUMENT_LOGO_PATH=./assets/acme_logo.png
DEFAULT_TEMPLATE_TYPE=sox_audit
```
Result: Documents show "Acme Corporation | Process Manager | Process Documentation" header with orange branding and company logo.

**Example 2: Adding Custom Template**
Edit `document_templates.json`:
```json
{
  "templates": {
    "security_review": {
      "name": "Security Review Report",
      "report_title": "Security Assessment",
      "sections": [
        {"number": 1, "title": "Scope", "key": "Scope"},
        {"number": 2, "title": "Findings", "key": "Findings"},
        {"number": 3, "title": "Recommendations", "key": "Recommendations"}
      ],
      "keywords": ["security", "vulnerability", "penetration"]
    }
  }
}
```

Set in `.env`:
```env
DEFAULT_TEMPLATE_TYPE=security_review
```

**Example 3: Programmatic Template Selection**
```python
from word_generator import create_process_document

filename = create_process_document(
    analysis_text="...",
    process_name="Model Deployment",
    template_type="mlops_workflow",
    metadata={"timestamp": "2026-02-07", "query": "Deploy model to production"}
)
```

### Integration Points

**config.py**:
- Loads and validates all template configuration
- Provides `get_brand_color_rgb()` helper for Word document colors
- Validates logo paths and color formats on startup

**word_generator.py**:
- Imports `Config` for branding values
- Loads `document_templates.json` on module initialization
- Dynamically generates sections based on template type

**app.py** (future enhancement):
- Could pass `template_type` parameter from frontend selection
- Currently uses `Config.DEFAULT_TEMPLATE_TYPE`

**gemini_client.py**:
- Query type detection (`_detect_query_type()`) could inform template selection
- Keywords from templates could be used for auto-detection

### Best Practices

**Template Design**:
- Use 3-7 sections for optimal readability
- Keep section titles concise (2-5 words)
- Choose unique section keys for regex matching
- Add descriptive keywords for auto-detection

**Branding Configuration**:
- Use web-safe colors (#RRGGBB format)
- Logo images should be PNG or JPG, ~500px wide
- Keep company names under 30 characters
- Test brand colors for readability (contrast with white background)

**Custom Templates**:
- Add to `document_templates.json` (no code changes needed)
- Follow existing JSON structure
- Set `DEFAULT_TEMPLATE_TYPE` in `.env` to activate
- Use meaningful template keys (lowercase, underscores)

**File Organization**:
- Keep logos in dedicated `assets/` folder
- Use descriptive filenames: `company_logo.png`
- Update `DOCUMENT_LOGO_PATH` with absolute or relative paths
- Commit `document_templates.json` to version control
- Do NOT commit `.env` (contains API keys)

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
   - Parse sections from response text using template configuration
   - Apply professional formatting (Calibri, proper spacing)
   - Add header with branding: "{COMPANY_NAME} | {PROJECT_NAME} | Process Documentation"
   - Use brand color from Config (default: #4A90E2)
   - Insert logo if configured in DOCUMENT_LOGO_PATH
   - Generate metadata table (timestamp, query, report type from template)
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

## Docker Containerization

### Docker Setup

**Dockerfile Features**:
- Based on `python:3.11-slim` for small image size
- Multi-stage optimized build
- Health checks every 30s
- Auto-creates necessary directories
- Non-root user in production

**Docker Compose (Development)**:
- Hot reload with code volume mounting
- Named volumes for data persistence (chroma_db, uploads, reports)
- Port forwarding: 5000:5000
- Auto-restart on failure
- Excludes virtual env from host machine

**Docker Compose (Production)**:
- No code mounting (immutable containers)
- Production environment variables
- Always restart policy
- Optimized for stability

### Makefile Commands

Run `make help` to see all commands:

```bash
make setup          # Create .env from template
make build          # Build Docker image
make up             # Start development environment
make up-prod        # Start production environment
make down           # Stop containers
make logs           # View application logs
make shell          # Access container bash shell
make clean          # Remove containers, volumes, images
make rebuild        # Rebuild and restart
make restart        # Restart application
make status         # Show container status
```

### VS Code Dev Container

**Features**:
- Automatic Python 3.11 environment setup
- Pre-installed VS Code extensions:
  - Python
  - Pylance
  - autopep8
  - ESLint
  - GitLens
  - GitHub Pull Requests
  - Code Spell Checker
- Git and GitHub CLI pre-installed
- Auto-formatting on save
- Integrated debugging

**Usage**:
1. Install "Remote - Containers" extension in VS Code
2. Open project folder
3. Press F1 → "Remote-Containers: Reopen in Container"
4. Wait for container build (first time only)
5. Start coding with fully configured environment

### Volume Persistence

Docker uses named volumes to persist data across container restarts:

- **chroma_data**: Vector database storage
- **uploads_data**: Temporary file uploads
- **reports_data**: Generated Word documents

Data persists even when containers are stopped or removed.

### Health Checks

Built-in health monitoring:
- Checks `/health` endpoint every 30s
- 10s timeout
- 3 retries before marking unhealthy
- 5s startup grace period (10s in production)

### Security Considerations

- `.env` file excluded from Docker build (`.dockerignore`)
- Use Docker secrets in production for sensitive data
- Container runs as non-root user in production
- Minimal base image reduces attack surface
- Health checks ensure service availability

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

The application maintains backward compatibility through:

1. **Legacy function wrappers**: `create_sox_word_document()` wraps `create_process_document()`
2. **Template system**: New templates added without modifying existing code
3. **Configuration defaults**: Safe fallback values for all new config options
4. **Feature flags**: Optional features can be disabled (e.g., MLOPS_FEATURES_ENABLED)

**Breaking Changes to Avoid**:
- Don't remove SOX template or keywords
- Don't change API endpoint URLs
- Don't modify existing database schema
- Don't change file upload formats

## MLOps Features (Phase 4 - Isolated Implementation)

### Overview

Complete MLOps (Machine Learning Operations) support added as an isolated, optional feature set with zero impact on existing functionality. All MLOps features are controlled by the `MLOPS_FEATURES_ENABLED` flag and implemented in separate modules.

### MLOps Documentation Templates

**Location**: `templates/mlops/`

Four comprehensive markdown templates for ML workflow documentation:

#### 1. mlops_guide.md (10 sections, ~50 KB)
Complete ML lifecycle best practices guide:
- Model development and version control
- Experiment tracking (MLflow, Weights & Biases, Neptune, TensorBoard)
- Training best practices and reproducibility
- Model validation strategies (metrics, testing, fairness analysis)
- Deployment strategies (Blue-Green, Canary, Rolling, Shadow)
- Monitoring and observability (drift detection, alerting)
- Model retraining triggers and workflows
- Security and compliance (model encryption, PII protection)
- Common pitfalls and best practices

#### 2. model_validation_template.md (11 sections, ~25 KB)
Structured validation report template:
- Executive summary with validation status
- Model overview and business context
- Validation data description and quality metrics
- Validation methodology (unit, integration, performance, regression)
- Performance metrics (classification, regression, latency, throughput)
- Comparison with baseline models
- Bias and fairness analysis across demographic groups
- Failure pattern analysis and root cause investigation
- Risk assessment and mitigation strategies
- Deployment recommendations and requirements checklist
- Approval sign-off section

#### 3. deployment_checklist.md (~40 KB)
Comprehensive pre-deployment checklist covering:
- Model readiness verification (validation, versioning, artifacts)
- Documentation requirements (model card, API docs, runbook)
- Security and compliance checks (authentication, vulnerability scanning, GDPR/HIPAA)
- Monitoring and observability setup (alerts, dashboards, logging)
- Testing requirements (functional, performance, integration, chaos)
- Deployment strategy selection and configuration
- Rollback plan and procedures
- Data management (input validation, output format)
- Performance optimization (quantization, auto-scaling, caching)
- Business continuity (high availability, disaster recovery)
- Stakeholder communication and training

#### 4. monitoring_guide.md (12 sections, ~35 KB)
Production monitoring strategies:
- Model performance metrics tracking (accuracy, latency, throughput)
- Data drift detection methods (K-S test, Chi-squared, PSI)
- Prediction drift monitoring
- Data quality monitoring (completeness, validity, consistency)
- Infrastructure and resource monitoring
- Error monitoring and classification
- Alert configuration with severity levels (P0-P3)
- Dashboard design (operations, performance, data quality)
- Model retraining triggers (performance, drift, time-based)
- Incident response procedures and runbooks
- Best practices and tool recommendations

**Usage as RAG Documents**:
- Upload any of these templates to enhance ML-specific queries
- System provides expert guidance on MLOps workflows
- No code changes required - pure documentation

### MLOps GitHub Actions Workflows

**Location**: `.github/workflows/mlops/`

Two isolated workflow files for automated ML documentation:

#### mlops-model-validation.yml
**Purpose**: Generate model validation reports

**Manual Dispatch Inputs**:
- `model_name` (required): Model identifier
- `model_version` (required): Semantic version (X.Y.Z)
- `validation_type` (choice): unit | integration | performance | regression
- `dataset_info` (optional): Dataset description
- `metrics_json` (optional): JSON string of metrics `{"accuracy": 0.95, "f1": 0.93}`

**Process**:
1. Sets up Python 3.11 environment
2. Installs python-docx
3. Generates 5-section validation report:
   - Model Overview
   - Data Pipeline
   - Training Process
   - Validation Results (with metrics parsing)
   - Deployment Plan
4. Applies GitHub Process Manager branding
5. Uploads artifact: `mlops-validation-report`

**Artifact Name**: `mlops-validation-{model-name}-v{version}.docx`

**Validation Logic**:
- Parses metrics JSON if provided
- Determines validation status: PASS (accuracy >= 0.90), CONDITIONAL PASS (>= 0.85), FAIL (< 0.85)
- Provides deployment recommendations based on metrics

#### mlops-deployment-doc.yml
**Purpose**: Generate deployment documentation

**Manual Dispatch Inputs**:
- `model_name` (required): Model to deploy
- `model_version` (required): Version number
- `deployment_target` (choice): staging | production | canary | development
- `deployment_strategy` (choice): blue-green | canary | rolling | shadow
- `deployment_config` (optional): Additional config as JSON

**Process**:
1. Sets up Python 3.11 environment
2. Generates 5-section deployment plan:
   - Model Overview
   - Data Pipeline (production integration)
   - Training Process (pre-deployment summary)
   - Validation Results (pre-deployment status)
   - Deployment Plan (strategy-specific steps)
3. Includes pre-deployment checklist
4. Provides monitoring plan and rollback procedures
5. Uploads artifact: `mlops-deployment-docs`

**Artifact Name**: `mlops-deployment-{model-name}-v{version}-{target}.docx`

**Strategy-Specific Content**:
- Canary: 10% → 50% → 100% rollout plan
- Blue-Green: Environment switch procedure
- Rolling: Gradual pod/instance replacement
- Shadow: Parallel deployment for comparison

**Triggering from UI**:
1. Navigate to Settings → GitHub Actions
2. Load workflows (new MLOps workflows appear)
3. Click trigger on desired workflow
4. Fill in parameters and execute
5. Download generated document from artifacts

### MLOps Helper Module

**File**: `mlops_helpers.py` (standalone, isolated module)

**Design Principles**:
- No imports from app.py, gemini_client, github_client, or rag_engine
- Only imported when MLOps features are explicitly used (lazy loading)
- Pure utility functions with no side effects
- Comprehensive error handling

**Functions**:

#### parse_ml_metrics(metrics_json: Union[str, Dict]) -> Dict
Parse and standardize ML metrics from various formats.

**Supported Input Formats**:
- JSON string: `'{"accuracy": 0.95, "f1_score": 0.93}'`
- Python dict: `{"accuracy": 0.95}`
- MLflow format: `{"metrics.accuracy": 0.95}`

**Standardized Output Metrics**:
- Classification: accuracy, precision, recall, f1_score, auc_roc
- Regression: mae, rmse, r2_score
- Training: loss
- Custom metrics: preserved with normalized names

**Key Normalization**:
- Case-insensitive matching
- Handles aliases: `acc` → `accuracy`, `f1` → `f1_score`
- Returns `'N/A'` for missing values

#### format_ml_metrics_for_document(metrics: Dict) -> str
Convert metrics dict to formatted Markdown for Word documents.

**Output Example**:
```
**Model Performance Metrics:**

• Accuracy: 0.9500
• Precision: 0.9400
• Recall: 0.9300
• F1 Score: 0.9350
```

**Features**:
- Ordered presentation (accuracy first, then precision/recall/f1)
- Formatted floating-point numbers (4 decimal places)
- Skips 'N/A' values
- Capitalizes metric names
- Includes custom metrics at end

#### validate_metrics_schema(metrics: Dict, required_metrics: Optional[List[str]]) -> tuple[bool, List[str]]
Validate that required metrics are present.

**Parameters**:
- `metrics`: Dictionary of metric values
- `required_metrics`: List of required metric names (default: `['accuracy']`)

**Returns**:
- `(is_valid: bool, missing_metrics: List[str])`

**Example**:
```python
valid, missing = validate_metrics_schema(
    {"accuracy": 0.95}, 
    ["accuracy", "f1_score"]
)
# Returns: (False, ['f1_score'])
```

#### calculate_model_score(metrics: Dict, weights: Optional[Dict[str, float]]) -> float
Calculate weighted model score from multiple metrics.

**Default Weights**:
```python
{
    'accuracy': 0.4,
    'precision': 0.2,
    'recall': 0.2,
    'f1_score': 0.2
}
```

**Returns**: Weighted score between 0.0 and 1.0

**Use Case**: Single-number model comparison across multiple metrics

#### get_metrics_summary(metrics: Dict) -> str
Generate human-readable summary of model performance.

**Output Examples**:
- "Model shows excellent accuracy (95.00%), strong F1 score (0.930), well-balanced precision and recall."
- "Model shows acceptable accuracy (87.00%), moderate F1 score (0.850)."

**Logic**:
- Accuracy: >= 0.95 (excellent), >= 0.90 (good), >= 0.85 (acceptable), < 0.85 (low)
- F1 score: >= 0.90 (strong), >= 0.80 (moderate)
- Precision/Recall: Checks balance (< 5% difference = balanced)

#### export_metrics_to_mlflow_format(metrics: Dict, run_name: str) -> Dict
Convert metrics to MLflow-compatible format for experiment tracking integration.

**Output Format**:
```json
{
  "run_name": "model_run",
  "metrics": {
    "metrics.accuracy": 0.95,
    "metrics.f1_score": 0.93
  },
  "params": {},
  "tags": {}
}
```

### MLOps API Endpoints

**Section Marker**: `# MLOps-Specific Endpoints (Isolated Section)` in app.py

All endpoints protected by feature flag check and isolated from core functionality.

#### GET /api/mlops/status
Check MLOps feature availability and configuration.

**Response**:
```json
{
  "enabled": true,
  "templates_dir": "templates/mlops",
  "templates_available": true,
  "template_count": 4,
  "workflows_dir": ".github/workflows/mlops",
  "workflows_available": true,
  "workflow_count": 2
}
```

**Use Case**: Frontend checks if MLOps section should be displayed

#### POST /api/mlops/parse-metrics
Parse and format ML metrics JSON.

**Request**:
```json
{
  "metrics": "{\"accuracy\": 0.95, \"f1\": 0.93, \"precision\": 0.94}"
}
```

**Response**:
```json
{
  "success": true,
  "parsed_metrics": {
    "accuracy": 0.95,
    "f1_score": 0.93,
    "precision": 0.94,
    "recall": "N/A",
    "auc_roc": "N/A",
    "loss": "N/A"
  },
  "formatted_text": "**Model Performance Metrics:**\n\n• Accuracy: 0.9500\n...",
  "summary": "Model shows excellent accuracy (95.00%), strong F1 score (0.930)..."
}
```

**Features**:
- Lazy imports mlops_helpers (only loaded when endpoint called)
- Feature flag protection (403 if not enabled)
- Comprehensive error handling

#### POST /api/mlops/validate-metrics
Validate ML metrics against schema.

**Request**:
```json
{
  "metrics": {"accuracy": 0.95, "f1_score": 0.93},
  "required": ["accuracy", "f1_score"]
}
```

**Response**:
```json
{
  "success": true,
  "valid": true,
  "missing_metrics": [],
  "overall_score": 0.94,
  "metrics": {"accuracy": 0.95, "f1_score": 0.93}
}
```

**Use Case**: Pre-deployment validation checks

#### GET /api/mlops/templates
List available MLOps documentation templates.

**Response**:
```json
{
  "templates": [
    {
      "name": "mlops_guide.md",
      "path": "templates/mlops/mlops_guide.md",
      "size_kb": 51.23
    },
    {
      "name": "model_validation_template.md",
      "path": "templates/mlops/model_validation_template.md",
      "size_kb": 24.67
    },
    ...
  ],
  "count": 4,
  "directory": "templates/mlops"
}
```

**Use Case**: Settings UI displays available templates with sizes

### MLOps Configuration

**Environment Variables** (`.env.template`):
```env
## MLOps Configuration (Optional - for ML workflow features)
# Enable or disable MLOps-specific features
MLOPS_FEATURES_ENABLED=false

# Directory containing MLOps documentation templates
MLOPS_TEMPLATES_DIR=templates/mlops

# Directory containing MLOps GitHub Actions workflows
MLOPS_WORKFLOWS_DIR=.github/workflows/mlops
```

**Config Class** (`config.py`):
```python
# MLOps-specific configuration (optional, isolated from core features)
MLOPS_FEATURES_ENABLED = os.getenv('MLOPS_FEATURES_ENABLED', 'false').lower() == 'true'
MLOPS_TEMPLATES_DIR = os.getenv('MLOPS_TEMPLATES_DIR', 'templates/mlops')
MLOPS_WORKFLOWS_DIR = os.getenv('MLOPS_WORKFLOWS_DIR', '.github/workflows/mlops')
```

**Default State**: Disabled (`false`) - no impact on existing functionality

### MLOps Settings UI Section

**Location**: `templates/settings.html`

**Dynamic Section** (only visible when `MLOPS_FEATURES_ENABLED=true`):

**Displays**:
- MLOps feature status (Enabled/Disabled)
- Template count (number of .md files in templates/mlops/)
- Workflow count (number of .yml files in .github/workflows/mlops/)
- List of available template files with sizes
- Helpful tip about uploading templates as RAG documents

**JavaScript**:
- `checkMLOpsStatus()`: Calls `/api/mlops/status` endpoint
- `loadMLOpsTemplates()`: Calls `/api/mlops/templates` endpoint
- Automatically hides section if features are disabled
- No interference with existing UI elements

**Implementation**:
```javascript
// Isolated JavaScript section
async function checkMLOpsStatus() {
    const response = await fetch('/api/mlops/status');
    if (response.ok && data.enabled) {
        mlopsSection.style.display = 'block';
        // Load and display template info
    } else {
        mlopsSection.style.display = 'none';
    }
}
```

### MLOps Isolation Guarantees

✅ **Zero Breaking Changes**:
- No modifications to existing Python modules (app.py, gemini_client.py, github_client.py, etc.)
- No changes to existing HTML/CSS/JavaScript outside isolated sections
- No modifications to existing database schema
- No changes to existing API routes
- All existing templates continue working

✅ **Complete Feature Isolation**:
- Separate directory: `templates/mlops/`
- Separate workflows: `.github/workflows/mlops/`
- Standalone module: `mlops_helpers.py`
- Feature flag: `MLOPS_FEATURES_ENABLED` (default: false)
- Lazy loading: mlops_helpers only imported when endpoints called
- UI sections: Hidden when disabled

✅ **Easy Rollback**:
To completely remove MLOps features:
1. Set `MLOPS_FEATURES_ENABLED=false` in `.env` (instant disable)
2. Or delete files:
   - `mlops_helpers.py`
   - `templates/mlops/` directory
   - `.github/workflows/mlops/` directory
3. Remove MLOps sections from:
   - `app.py` (lines marked with "MLOps-Specific Endpoints")
   - `templates/settings.html` (MLOps section)

**Result**: Application returns to pre-MLOps state with zero residual code

### MLOps Usage Examples

**Example 1: Upload MLOps Templates as RAG Documents**
```
1. Navigate to Chat page
2. Upload templates/mlops/mlops_guide.md
3. Ask: "What metrics should I track for a classification model?"
4. System provides expert guidance from uploaded template
```

**Example 2: Generate Model Validation Report**
```
1. Go to Settings → GitHub Actions
2. Trigger "MLOps Model Validation Report" workflow
3. Inputs:
   - Model Name: fraud-detector
   - Model Version: 2.1.0
   - Validation Type: performance
   - Metrics: {"accuracy": 0.952, "f1": 0.938, "precision": 0.945, "recall": 0.932}
4. Download generated .docx from artifacts
```

**Example 3: Use API to Parse Metrics**
```bash
curl -X POST http://localhost:5000/api/mlops/parse-metrics \
  -H "Content-Type: application/json" \
  -d '{"metrics": "{\"accuracy\": 0.95, \"f1\": 0.93}"}'
```

**Example 4: Chat with MLOps Context**
```
Query: "Create a deployment checklist for my recommendation model"
Response: Detailed checklist based on deployment_checklist.md template
         with model-specific considerations
```

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
- [x] Docker containerization
- [x] VS Code Dev Container support
- [ ] Kubernetes deployment manifests
- [ ] Authentication/multi-user support
- [ ] Streaming responses from Gemini
- [ ] Code syntax highlighting in responses
- [x] Multi-template support (SOX, MLOps, DevOps, Generic)
- [x] Word document generation
- [x] GitHub Actions workflow triggers
- [x] AI system prompt customization (6 templates + custom)
- [x] Template configuration via JSON files (Phase 3)
- [x] Logo upload and customization (Phase 3)
- [x] Company branding configuration (Phase 3)
- [ ] Custom template editor in UI
- [ ] Integration tests with Docker
- [ ] CI/CD pipeline for Docker builds
- [ ] Multi-architecture Docker images (ARM64)

## Links & Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: February 7, 2026  
**Python Version**: 3.8+ (3.11 recommended)  
**Docker**: ✅ Fully Containerized  
**Phase 3**: ✅ Document Template System Complete  
**Status**: ✅ Fully Production Ready  
**Project**: GitHub Process Manager (formerly "Local AI RAG Chatbot")  
**Project**: GitHub Process Manager (formerly "Local AI RAG Chatbot")