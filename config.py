"""
Configuration module for the RAG Chatbot.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv
from logger import logger

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # RAG Configuration
    CHUNK_SIZE = 800  # Characters per chunk
    CHUNK_OVERLAP = 200  # Overlap between chunks
    TOP_K_RESULTS = 3  # Number of relevant chunks to retrieve
    
    # Gemini Model Configuration
    GEMINI_MODEL = 'gemini-2.5-flash'  # Latest stable Gemini 2.5 Flash model
    GEMINI_EMBEDDING_MODEL = 'models/text-embedding-004'
    TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
    MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', '2048'))
    
    # System Prompt Configuration
    SYSTEM_PROMPT_TEMPLATE = os.getenv('SYSTEM_PROMPT_TEMPLATE', 'default')
    CUSTOM_SYSTEM_PROMPT = os.getenv('CUSTOM_SYSTEM_PROMPT', '')
    
    # Document Template Configuration (Phase 3)
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'GitHub Process Manager')
    COMPANY_NAME = os.getenv('COMPANY_NAME', '')
    BRAND_COLOR = os.getenv('BRAND_COLOR', '#4A90E2')
    DOCUMENT_LOGO_PATH = os.getenv('DOCUMENT_LOGO_PATH', '')
    DEFAULT_TEMPLATE_TYPE = os.getenv('DEFAULT_TEMPLATE_TYPE', 'generic')
    DOCUMENT_TEMPLATES_PATH = os.getenv('DOCUMENT_TEMPLATES_PATH', 'document_templates.json')
    
    # MLOps-specific configuration (optional, isolated from core features)
    MLOPS_FEATURES_ENABLED = os.getenv('MLOPS_FEATURES_ENABLED', 'false').lower() == 'true'
    MLOPS_TEMPLATES_DIR = os.getenv('MLOPS_TEMPLATES_DIR', 'templates/mlops')
    MLOPS_WORKFLOWS_DIR = os.getenv('MLOPS_WORKFLOWS_DIR', '.github/workflows/mlops')
    
    # Pre-defined System Prompt Templates
    SYSTEM_PROMPTS = {
        'default': (
            "You are a helpful AI assistant with access to reference documents "
            "and GitHub repository information. Provide accurate, concise answers "
            "based on the provided context. If the context doesn't contain relevant "
            "information, say so clearly."
        ),
        'technical': (
            "You are a senior technical documentation expert and software architect. "
            "Analyze code, documentation, and technical processes with deep expertise. "
            "Provide detailed technical insights, best practices, and architectural "
            "recommendations. Use precise technical terminology and cite specific "
            "documentation when available. If information is missing, clearly state "
            "what additional context would be helpful."
        ),
        'auditor': (
            "You are an experienced compliance auditor and risk assessment expert. "
            "Focus on control effectiveness, risk mitigation, and regulatory compliance. "
            "Provide thorough analysis of controls, identify gaps, and recommend "
            "remediation actions. Structure responses with clear findings, evidence, "
            "and actionable recommendations. Maintain professional audit documentation "
            "standards."
        ),
        'developer': (
            "You are an expert software developer and DevOps engineer. "
            "Provide practical code solutions, debugging assistance, and best practices "
            "for software development. Focus on code quality, performance, security, "
            "and maintainability. Use code examples when helpful and explain complex "
            "concepts clearly. Reference documentation and industry standards."
        ),
        'analyst': (
            "You are a business analyst and process improvement consultant. "
            "Analyze workflows, identify inefficiencies, and recommend optimizations. "
            "Provide structured analysis with clear problem statements, root causes, "
            "and actionable solutions. Use data-driven insights and reference best "
            "practices in process management."
        ),
        'educator': (
            "You are an experienced technical educator and mentor. "
            "Explain concepts clearly and progressively, adapting to different "
            "knowledge levels. Use examples, analogies, and step-by-step breakdowns. "
            "Encourage learning by asking clarifying questions and suggesting "
            "additional resources. Make complex topics accessible and engaging."
        )
    }
    
    @staticmethod
    def validate_color_format(color_string):
        """Validate hex color format (#RRGGBB)."""
        import re
        if not color_string:
            return True  # Empty is allowed
        pattern = r'^#[0-9A-Fa-f]{6}$'
        return bool(re.match(pattern, color_string))
    
    @staticmethod
    def validate_logo_path(logo_path):
        """Validate logo file exists if path is provided."""
        if not logo_path:
            return True  # Empty is allowed
        if os.path.exists(logo_path):
            # Check if it's an image file
            valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
            _, ext = os.path.splitext(logo_path)
            if ext.lower() in valid_extensions:
                return True
            else:
                logger.warning(f"Logo file {logo_path} has unsupported format. Use: {valid_extensions}")
                return False
        else:
            logger.warning(f"Logo file not found: {logo_path}")
            return False
    
    @staticmethod
    def validate():
        """Validate critical configuration settings."""
        errors = []
        
        if not Config.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set. Please add it to your .env file.")
        
        if not Config.GITHUB_TOKEN:
            logger.warning("GITHUB_TOKEN is not set. GitHub features will be limited.")
        
        if not Config.GITHUB_REPO_URL:
            logger.warning("GITHUB_REPO_URL is not set. Please configure it to use GitHub features.")
        
        # Validate brand color format
        if not Config.validate_color_format(Config.BRAND_COLOR):
            errors.append(f"BRAND_COLOR '{Config.BRAND_COLOR}' is not a valid hex color (format: #RRGGBB)")
        
        # Validate logo path if provided
        if Config.DOCUMENT_LOGO_PATH and not Config.validate_logo_path(Config.DOCUMENT_LOGO_PATH):
            logger.warning(f"DOCUMENT_LOGO_PATH is set but invalid. Logo will be skipped.")
        
        # Validate template type
        valid_templates = {'sox_audit', 'mlops_workflow', 'devops_pipeline', 'generic'}
        if Config.DEFAULT_TEMPLATE_TYPE not in valid_templates:
            logger.warning(f"DEFAULT_TEMPLATE_TYPE '{Config.DEFAULT_TEMPLATE_TYPE}' not recognized. Using 'generic'.")
            Config.DEFAULT_TEMPLATE_TYPE = 'generic'
        
        if errors:
            error_msg = "\n".join(errors)
            logger.error(f"Configuration validation failed:\n{error_msg}")
            raise ValueError(f"Configuration errors:\n{error_msg}")
        
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
        os.makedirs('generated_reports', exist_ok=True)
        
        logger.info("Configuration validated successfully")
        return True
    
    @staticmethod
    def get_system_prompt():
        """Get the active system prompt based on configuration."""
        # Custom prompt takes precedence
        if Config.CUSTOM_SYSTEM_PROMPT:
            return Config.CUSTOM_SYSTEM_PROMPT
        
        # Use template from config
        template = Config.SYSTEM_PROMPT_TEMPLATE
        return Config.SYSTEM_PROMPTS.get(template, Config.SYSTEM_PROMPTS['default'])
    
    @staticmethod
    def get_available_prompts():
        """Get list of available prompt templates."""
        return list(Config.SYSTEM_PROMPTS.keys())
    
    @staticmethod
    def get_brand_color_rgb():
        """Convert brand color hex to RGB tuple for Word documents."""
        hex_color = Config.BRAND_COLOR.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
