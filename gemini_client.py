"""
Gemini API client for chat functionality.
Handles query processing with RAG context and GitHub data.
"""
import google.generativeai as genai
from logger import logger
from config import Config

class GeminiClient:
    """Client for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            
            # Configure generation settings
            self.generation_config = {
                'temperature': Config.TEMPERATURE,
                'max_output_tokens': Config.MAX_OUTPUT_TOKENS,
            }
            
            logger.info("Gemini client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def generate_response(self, user_query, rag_context=None, github_data=None):
        """
        Generate response using Gemini with RAG context and GitHub data.
        
        Args:
            user_query: User's question/query
            rag_context: List of relevant document chunks from RAG
            github_data: Relevant GitHub repository data
        
        Returns:
            Generated response text
        """
        try:
            # Build comprehensive prompt
            prompt = self._build_prompt(user_query, rag_context, github_data)
            
            logger.info(f"Generating response for query: {user_query[:100]}...")
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Extract text from response
            response_text = response.text
            
            logger.info("Response generated successfully")
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _build_prompt(self, user_query, rag_context=None, github_data=None):
        """
        Build comprehensive prompt with context.
        
        Args:
            user_query: User's question
            rag_context: RAG document chunks
            github_data: GitHub repository data
        
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        # Detect query type for structured responses
        query_type = self._detect_query_type(user_query)
        
        # System instruction
        prompt_parts.append(
            "You are a helpful AI assistant with access to reference documents "
            "and GitHub repository information. Provide accurate, concise answers "
            "based on the provided context. If the context doesn't contain relevant "
            "information, say so clearly."
        )
        
        # Add type-specific instructions for structured responses
        if query_type == 'sox_audit':
            prompt_parts.append(self._get_sox_audit_instructions())
        elif query_type == 'mlops_workflow':
            prompt_parts.append(self._get_mlops_instructions())
        elif query_type == 'devops_pipeline':
            prompt_parts.append(self._get_devops_instructions())
        # For 'generic' type, no special structure needed
        
        # Add RAG context if available
        if rag_context and len(rag_context) > 0:
            prompt_parts.append("\n\n=== REFERENCE DOCUMENTS ===")
            for i, chunk in enumerate(rag_context, 1):
                filename = chunk.get('metadata', {}).get('filename', 'Unknown')
                text = chunk.get('text', '')
                prompt_parts.append(f"\n[Document {i}: {filename}]\n{text}")
        
        # Add GitHub context if available
        if github_data:
            prompt_parts.append("\n\n=== GITHUB REPOSITORY DATA ===")
            
            if 'repository_info' in github_data:
                info = github_data['repository_info']
                prompt_parts.append(f"\nRepository: {info.get('name', 'N/A')}")
                prompt_parts.append(f"Description: {info.get('description', 'N/A')}")
                prompt_parts.append(f"Stars: {info.get('stars', 'N/A')}")
            
            if 'pull_requests' in github_data:
                prs = github_data['pull_requests']
                prompt_parts.append(f"\n\nRecent Pull Requests ({len(prs)}):")
                for pr in prs[:5]:  # Limit to 5 PRs
                    prompt_parts.append(f"- #{pr.get('number')}: {pr.get('title')} ({pr.get('state')})")
            
            if 'issues' in github_data:
                issues = github_data['issues']
                prompt_parts.append(f"\n\nRecent Issues ({len(issues)}):")
                for issue in issues[:5]:  # Limit to 5 issues
                    prompt_parts.append(f"- #{issue.get('number')}: {issue.get('title')} ({issue.get('state')})")
            
            if 'workflows' in github_data:
                workflows = github_data['workflows']
                prompt_parts.append(f"\n\nWorkflow Runs ({len(workflows)}):")
                for wf in workflows[:3]:  # Limit to 3 workflows
                    prompt_parts.append(f"- {wf.get('name')}: {wf.get('conclusion', 'running')}")
            
            if 'files' in github_data:
                files = github_data['files']
                prompt_parts.append(f"\n\nRepository Files: {', '.join(files[:10])}")
        
        # Add user query
        prompt_parts.append(f"\n\n=== USER QUESTION ===\n{user_query}")
        
        # Add instruction for response
        prompt_parts.append(
            "\n\nPlease provide a helpful and accurate response based on the information above. "
            "Cite specific documents or GitHub data when relevant."
        )
        
        return "\n".join(prompt_parts)
    
    def test_connection(self):
        """
        Test Gemini API connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.model.generate_content(
                "Respond with 'OK' if you can read this message.",
                generation_config={'max_output_tokens': 10}
            )
            logger.info("Gemini API connection test successful")
            return True
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {e}")
            return False
    
    def _detect_query_type(self, query):
        """
        Detect the type of query to apply appropriate response structure.
        
        Returns:
            str: 'sox_audit', 'mlops_workflow', 'devops_pipeline', or 'generic'
        """
        query_lower = query.lower()
        
        # SOX/Audit keywords
        sox_keywords = ['sox control', 'control analysis', 'control objective', 
                       'testing procedure', 'sox', 'control test', 'audit', 
                       'compliance', 'internal control']
        
        # MLOps keywords
        mlops_keywords = ['model', 'mlops', 'machine learning', 'training', 
                         'inference', 'dataset', 'ml pipeline', 'model deployment',
                         'feature engineering', 'hyperparameter', 'ml workflow']
        
        # DevOps keywords
        devops_keywords = ['pipeline', 'ci/cd', 'deployment', 'build', 'release',
                          'devops', 'kubernetes', 'docker', 'container', 'jenkins',
                          'gitlab ci', 'github actions']
        
        # Check for each type
        if any(keyword in query_lower for keyword in sox_keywords):
            return 'sox_audit'
        elif any(keyword in query_lower for keyword in mlops_keywords):
            return 'mlops_workflow'
        elif any(keyword in query_lower for keyword in devops_keywords):
            return 'devops_pipeline'
        else:
            return 'generic'
    
    def _get_sox_audit_instructions(self):
        """SOX audit structured response instructions."""
        return (
            "\n\n**IMPORTANT: SOX Control Analysis Structure**\n"
            "When analyzing SOX controls, structure your response with these 5 sections:\n\n"
            "1. Control Objective\n"
            "   - Clearly state what the control aims to achieve\n"
            "   - Describe the purpose and scope\n\n"
            "2. Risks Addressed\n"
            "   - List specific risks mitigated by this control\n"
            "   - Use bullet points for clarity\n\n"
            "3. Testing Procedures\n"
            "   - Provide step-by-step testing procedures\n"
            "   - Include sample size and selection criteria\n"
            "   - Detail what evidence to examine\n\n"
            "4. Test Results and Findings\n"
            "   - Report observations from testing\n"
            "   - Note any exceptions or issues identified\n"
            "   - Include quantitative results (e.g., 25/25 samples passed)\n\n"
            "5. Conclusion and Recommendation\n"
            "   - Provide overall assessment of control effectiveness\n"
            "   - Recommend any remediation actions if needed\n"
            "   - State whether control is operating effectively\n\n"
            "Use numbered headings exactly as shown above for consistency."
        )
    
    def _get_mlops_instructions(self):
        """MLOps workflow structured response instructions."""
        return (
            "\n\n**IMPORTANT: MLOps Workflow Documentation Structure**\n"
            "When documenting ML workflows, structure your response with these 5 sections:\n\n"
            "1. Model Overview\n"
            "   - Describe model architecture and purpose\n"
            "   - Define inputs, outputs, and use case\n\n"
            "2. Data Pipeline\n"
            "   - Detail data sources and preprocessing steps\n"
            "   - Explain data validation and quality checks\n"
            "   - Describe feature engineering process\n\n"
            "3. Training Process\n"
            "   - Document training methodology\n"
            "   - Specify hyperparameters and configurations\n"
            "   - Describe experiment tracking approach\n\n"
            "4. Validation Results\n"
            "   - Report performance metrics (accuracy, F1, etc.)\n"
            "   - Include test dataset results\n"
            "   - Document any model limitations or biases\n\n"
            "5. Deployment Plan\n"
            "   - Specify serving infrastructure\n"
            "   - Describe monitoring and alerting strategy\n"
            "   - Define rollback procedures\n\n"
            "Use numbered headings exactly as shown above for consistency."
        )
    
    def _get_devops_instructions(self):
        """DevOps pipeline structured response instructions."""
        return (
            "\n\n**IMPORTANT: DevOps Pipeline Documentation Structure**\n"
            "When documenting DevOps pipelines, structure your response with these 5 sections:\n\n"
            "1. Pipeline Overview\n"
            "   - Describe pipeline purpose and triggers\n"
            "   - Define pipeline stages and flow\n\n"
            "2. Build Steps\n"
            "   - Detail compilation and build process\n"
            "   - List dependencies and build tools\n"
            "   - Describe artifact generation\n\n"
            "3. Test and Quality Gates\n"
            "   - Document test suites (unit, integration, e2e)\n"
            "   - Specify quality metrics and thresholds\n"
            "   - Describe security scanning steps\n\n"
            "4. Deployment Process\n"
            "   - Define deployment stages (dev, staging, prod)\n"
            "   - Specify deployment strategy (blue-green, canary, etc.)\n"
            "   - Document approval requirements\n\n"
            "5. Monitoring and Rollback\n"
            "   - Describe post-deployment monitoring\n"
            "   - Define success criteria\n"
            "   - Specify rollback procedures and triggers\n\n"
            "Use numbered headings exactly as shown above for consistency."
        )
