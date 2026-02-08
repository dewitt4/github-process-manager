"""
Flask application for Local AI RAG Chatbot.
Main application file with routes and handlers.
"""
from flask import Flask, render_template, request, jsonify, session, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from config import Config
from logger import logger
from rag_engine import RAGEngine
from gemini_client import GeminiClient
from github_client import GitHubClient
from word_generator import create_process_document, list_generated_reports, cleanup_old_reports

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
try:
    Config.validate()
    rag_engine = RAGEngine()
    gemini_client = GeminiClient()
    github_client = GitHubClient()
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize application: {e}")
    raise

@app.route('/')
def index():
    """Render main chat interface."""
    return render_template('index.html')

@app.route('/settings')
def settings():
    """Render settings page."""
    repo_info = github_client.get_repository_info() if github_client.is_connected() else None
    rag_stats = rag_engine.get_stats()
    
    return render_template(
        'settings.html',
        repo_info=repo_info,
        rag_stats=rag_stats,
        github_connected=github_client.is_connected()
    )

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests.
    Combines RAG context and GitHub data to generate responses.
    """
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        logger.info(f"Processing chat query: {user_query[:100]}...")
        
        # Retrieve RAG context
        rag_context = rag_engine.retrieve_context(user_query)
        
        # Gather GitHub data if connected
        github_data = None
        if github_client.is_connected():
            github_data = {
                'repository_info': github_client.get_repository_info(),
                'pull_requests': github_client.get_pull_requests(state='open', limit=5),
                'issues': github_client.get_issues(state='open', limit=5)
            }
        
        # Generate response
        response = gemini_client.generate_response(
            user_query,
            rag_context=rag_context,
            github_data=github_data
        )
        
        return jsonify({
            'response': response,
            'rag_chunks_used': len(rag_context),
            'github_data_available': github_data is not None
        })
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Handle document uploads for RAG."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not Config.allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Supported: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filename}")
        
        # Process document
        chunks_added = rag_engine.add_document(filepath, filename)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Document processed successfully. Added {chunks_added} chunks.',
            'filename': filename,
            'chunks_added': chunks_added
        })
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/stats', methods=['GET'])
def rag_stats():
    """Get RAG database statistics."""
    try:
        stats = rag_engine.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting RAG stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/clear', methods=['POST'])
def clear_rag():
    """Clear RAG database."""
    try:
        success = rag_engine.clear_database()
        if success:
            return jsonify({'success': True, 'message': 'RAG database cleared'})
        else:
            return jsonify({'error': 'Failed to clear database'}), 500
    except Exception as e:
        logger.error(f"Error clearing RAG database: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/connect', methods=['POST'])
def connect_github():
    """Connect to a GitHub repository."""
    try:
        data = request.get_json()
        repo_url = data.get('repo_url', '').strip()
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        success = github_client.connect_to_repo(repo_url)
        
        if success:
            repo_info = github_client.get_repository_info()
            return jsonify({
                'success': True,
                'message': 'Connected to repository',
                'repo_info': repo_info
            })
        else:
            return jsonify({'error': 'Failed to connect to repository'}), 500
            
    except Exception as e:
        logger.error(f"Error connecting to GitHub: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/info', methods=['GET'])
def github_info():
    """Get GitHub repository information."""
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'Not connected to a repository'}), 404
        
        info = github_client.get_repository_info()
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Error getting GitHub info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/workflows', methods=['GET'])
def list_workflows():
    """List available GitHub Actions workflows."""
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'Not connected to a repository'}), 404
        
        workflows = github_client.list_workflows()
        return jsonify({'workflows': workflows})
        
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/workflow/trigger', methods=['POST'])
def trigger_workflow():
    """Manually trigger a GitHub Actions workflow."""
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'Not connected to a repository'}), 404
        
        data = request.get_json()
        workflow_id = data.get('workflow_id')
        ref = data.get('ref', 'main')
        inputs = data.get('inputs', {})
        
        if not workflow_id:
            return jsonify({'error': 'Workflow ID is required'}), 400
        
        success = github_client.trigger_workflow(workflow_id, ref, inputs)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Workflow {workflow_id} triggered on {ref}'
            })
        else:
            return jsonify({'error': 'Failed to trigger workflow'}), 500
            
    except Exception as e:
        logger.error(f"Error triggering workflow: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/pulls', methods=['GET'])
def get_pulls():
    """Get pull requests from repository."""
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'Not connected to a repository'}), 404
        
        state = request.args.get('state', 'open')
        limit = int(request.args.get('limit', 10))
        
        pulls = github_client.get_pull_requests(state, limit)
        return jsonify({'pull_requests': pulls})
        
    except Exception as e:
        logger.error(f"Error getting pull requests: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/issues', methods=['GET'])
def get_issues():
    """Get issues from repository."""
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'Not connected to a repository'}), 404
        
        state = request.args.get('state', 'open')
        limit = int(request.args.get('limit', 10))
        
        issues = github_client.get_issues(state, limit)
        return jsonify({'issues': issues})
        
    except Exception as e:
        logger.error(f"Error getting issues: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'gemini_connected': True,  # If we got here, Gemini is configured
        'github_connected': github_client.is_connected(),
        'rag_chunks': rag_engine.get_stats().get('total_chunks', 0)
    })

@app.route('/api/generate-word-report', methods=['POST'])
def generate_word_report():
    """
    Generate a Word document for process analysis.
    
    Request JSON:
        - analysis_text: The chatbot's analysis response
        - process_name: Name of the process (optional)
        - query: Original user query (optional)
        
    Returns:
        JSON with filename and download URL
    """
    try:
        data = request.get_json()
        analysis_text = data.get('analysis_text', '')
        process_name = data.get('process_name', 'Process Analysis')
        query = data.get('query', '')
        
        if not analysis_text:
            return jsonify({'error': 'No analysis text provided'}), 400
        
        # Prepare metadata
        metadata = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'query': query
        }
        
        # Generate Word document
        filename = create_process_document(analysis_text, process_name, metadata)
        
        logger.info(f"Generated Word report: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'download_url': f'/api/download/{filename}'
        })
        
    except Exception as e:
        logger.error(f"Error generating Word report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Serve generated Word documents for download.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File download response
    """
    try:
        # Sanitize filename
        filename = secure_filename(filename)
        filepath = os.path.join('generated_reports', filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/list', methods=['GET'])
def list_reports():
    """
    List all generated Word documents.
    
    Returns:
        JSON array of file information
    """
    try:
        reports = list_generated_reports()
        return jsonify({
            'success': True,
            'reports': reports
        })
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/cleanup', methods=['POST'])
def cleanup_reports():
    """
    Delete reports older than specified hours.
    
    Request JSON:
        - hours: Delete files older than this many hours (default: 24)
        
    Returns:
        JSON with number of files deleted
    """
    try:
        data = request.get_json() or {}
        hours = data.get('hours', 24)
        
        deleted_count = cleanup_old_reports(hours)
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Deleted {deleted_count} old report(s)'
        })
        
    except Exception as e:
        logger.error(f"Error cleaning up reports: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/process-analysis/trigger', methods=['POST'])
def trigger_process_analysis_workflow():
    """
    Trigger GitHub Actions workflow for process analysis.
    
    Request JSON:
        - process_name: Name of the process
        - process_data: Data for analysis
        - analysis_type: Type of analysis (optional)
        
    Returns:
        JSON with workflow run information
    """
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'GitHub not connected'}), 400
        
        data = request.get_json()
        process_name = data.get('process_name', 'Process Analysis')
        process_data = data.get('process_data', '')
        analysis_type = data.get('analysis_type', 'standard')
        
        # Trigger the workflow
        run_info = github_client.trigger_process_workflow(process_name, process_data, analysis_type)
        
        return jsonify({
            'success': True,
            'run_id': run_info.get('run_id'),
            'workflow_name': run_info.get('workflow_name'),
            'message': 'Workflow triggered successfully'
        })
        
    except Exception as e:
        logger.error(f"Error triggering SOX workflow: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/artifacts/check/<int:run_id>', methods=['GET'])
def check_workflow_artifacts(run_id):
    """
    Check for and download workflow artifacts.
    
    Args:
        run_id: GitHub Actions workflow run ID
        
    Returns:
        JSON with artifact status and download info
    """
    try:
        if not github_client.is_connected():
            return jsonify({'error': 'GitHub not connected'}), 400
        
        # Check for artifacts and download if available
        result = github_client.check_and_download_artifact(run_id, 'sox-report')
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error checking workflow artifacts: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
