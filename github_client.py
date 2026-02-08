"""
GitHub API client for repository integration.
Handles authentication and data retrieval from GitHub repositories.
"""
from github import Github, GithubException
from logger import logger
from config import Config

class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self):
        """Initialize GitHub client."""
        self.github = None
        self.repo = None
        self.token = Config.GITHUB_TOKEN
        self.repo_url = Config.GITHUB_REPO_URL
        
        if self.token:
            try:
                self.github = Github(self.token)
                
                # Test authentication
                user = self.github.get_user()
                logger.info(f"GitHub authenticated as: {user.login}")
                
                # Connect to repository if URL is configured
                if self.repo_url:
                    self._connect_repository(self.repo_url)
                    
            except GithubException as e:
                logger.error(f"GitHub authentication failed: {e}")
                raise
        else:
            logger.warning("GitHub token not configured. GitHub features will be unavailable.")
    
    def _connect_repository(self, repo_url):
        """
        Connect to a GitHub repository.
        
        Args:
            repo_url: Repository URL (https://github.com/owner/repo)
        """
        try:
            # Extract owner and repo name from URL
            parts = repo_url.rstrip('/').split('/')
            owner = parts[-2]
            repo_name = parts[-1]
            
            full_name = f"{owner}/{repo_name}"
            self.repo = self.github.get_repo(full_name)
            
            logger.info(f"Connected to repository: {full_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to repository {repo_url}: {e}")
            raise
    
    def connect_to_repo(self, repo_url):
        """
        Connect to a different repository.
        
        Args:
            repo_url: Repository URL
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._connect_repository(repo_url)
            self.repo_url = repo_url
            return True
        except Exception as e:
            logger.error(f"Error connecting to repository: {e}")
            return False
    
    def get_repository_info(self):
        """
        Get basic repository information.
        
        Returns:
            Dictionary with repository metadata
        """
        if not self.repo:
            return None
        
        try:
            return {
                'name': self.repo.full_name,
                'description': self.repo.description,
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'open_issues': self.repo.open_issues_count,
                'language': self.repo.language,
                'created_at': str(self.repo.created_at),
                'updated_at': str(self.repo.updated_at)
            }
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return None
    
    def get_pull_requests(self, state='open', limit=10):
        """
        Get pull requests from repository.
        
        Args:
            state: PR state ('open', 'closed', 'all')
            limit: Maximum number of PRs to retrieve
        
        Returns:
            List of pull request data
        """
        if not self.repo:
            return []
        
        try:
            prs = self.repo.get_pulls(state=state)
            pr_list = []
            
            for pr in prs[:limit]:
                pr_list.append({
                    'number': pr.number,
                    'title': pr.title,
                    'state': pr.state,
                    'author': pr.user.login,
                    'created_at': str(pr.created_at),
                    'updated_at': str(pr.updated_at),
                    'url': pr.html_url
                })
            
            logger.info(f"Retrieved {len(pr_list)} pull requests")
            return pr_list
            
        except Exception as e:
            logger.error(f"Error getting pull requests: {e}")
            return []
    
    def get_issues(self, state='open', limit=10):
        """
        Get issues from repository.
        
        Args:
            state: Issue state ('open', 'closed', 'all')
            limit: Maximum number of issues to retrieve
        
        Returns:
            List of issue data
        """
        if not self.repo:
            return []
        
        try:
            issues = self.repo.get_issues(state=state)
            issue_list = []
            
            for issue in issues[:limit]:
                # Skip pull requests (they appear in issues API)
                if issue.pull_request:
                    continue
                
                issue_list.append({
                    'number': issue.number,
                    'title': issue.title,
                    'state': issue.state,
                    'author': issue.user.login,
                    'created_at': str(issue.created_at),
                    'updated_at': str(issue.updated_at),
                    'labels': [label.name for label in issue.labels],
                    'url': issue.html_url
                })
            
            logger.info(f"Retrieved {len(issue_list)} issues")
            return issue_list
            
        except Exception as e:
            logger.error(f"Error getting issues: {e}")
            return []
    
    def get_workflow_runs(self, limit=5):
        """
        Get recent workflow runs.
        
        Args:
            limit: Maximum number of workflow runs to retrieve
        
        Returns:
            List of workflow run data
        """
        if not self.repo:
            return []
        
        try:
            workflows = self.repo.get_workflow_runs()
            workflow_list = []
            
            for wf in workflows[:limit]:
                workflow_list.append({
                    'id': wf.id,
                    'name': wf.name,
                    'status': wf.status,
                    'conclusion': wf.conclusion,
                    'created_at': str(wf.created_at),
                    'updated_at': str(wf.updated_at),
                    'url': wf.html_url
                })
            
            logger.info(f"Retrieved {len(workflow_list)} workflow runs")
            return workflow_list
            
        except Exception as e:
            logger.error(f"Error getting workflow runs: {e}")
            return []
    
    def get_repository_files(self, path='', limit=20):
        """
        Get files from repository.
        
        Args:
            path: Directory path in repository
            limit: Maximum number of files to retrieve
        
        Returns:
            List of file names
        """
        if not self.repo:
            return []
        
        try:
            contents = self.repo.get_contents(path)
            file_list = []
            
            for content in contents[:limit]:
                file_list.append(content.path)
            
            logger.info(f"Retrieved {len(file_list)} files from repository")
            return file_list
            
        except Exception as e:
            logger.error(f"Error getting repository files: {e}")
            return []
    
    def trigger_workflow(self, workflow_id, ref='main', inputs=None):
        """
        Manually trigger a GitHub Actions workflow.
        
        Args:
            workflow_id: Workflow ID or filename
            ref: Git reference (branch, tag)
            inputs: Dictionary of workflow inputs
        
        Returns:
            True if successful, False otherwise
        """
        if not self.repo:
            logger.error("No repository connected")
            return False
        
        try:
            workflow = self.repo.get_workflow(workflow_id)
            result = workflow.create_dispatch(ref=ref, inputs=inputs or {})
            
            logger.info(f"Triggered workflow: {workflow_id} on {ref}")
            return True
            
        except Exception as e:
            logger.error(f"Error triggering workflow: {e}")
            return False
    
    def list_workflows(self):
        """
        List all available workflows in the repository.
        
        Returns:
            List of workflow data
        """
        if not self.repo:
            return []
        
        try:
            workflows = self.repo.get_workflows()
            workflow_list = []
            
            for wf in workflows:
                workflow_list.append({
                    'id': wf.id,
                    'name': wf.name,
                    'path': wf.path,
                    'state': wf.state
                })
            
            logger.info(f"Retrieved {len(workflow_list)} workflows")
            return workflow_list
            
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            return []
    
    def is_connected(self):
        """Check if GitHub client is connected to a repository."""
        return self.github is not None and self.repo is not None
    
    def trigger_process_workflow(self, process_name, process_data, analysis_type='standard', workflow_file='process-analysis-doc.yml'):
        """
        Trigger the Process Analysis workflow.
        
        Args:
            process_name: Name of the process/control/workflow
            process_data: Process data and context
            analysis_type: Type of analysis (standard, detailed, summary)
            workflow_file: Workflow filename (default: process-analysis-doc.yml)
        
        Returns:
            Dictionary with workflow run information
        """
        if not self.repo:
            logger.error("No repository connected")
            raise Exception("GitHub repository not connected")
        
        try:
            workflow = self.repo.get_workflow(workflow_file)
            
            # Prepare inputs
            inputs = {
                'process_name': process_name,
                'process_data': process_data,
                'analysis_type': analysis_type
            }
            
            # Trigger workflow
            result = workflow.create_dispatch(ref='main', inputs=inputs)
            
            logger.info(f"Triggered process workflow for: {process_name}")
            
            # Get the latest run ID (this is approximate)
            import time
            time.sleep(2)  # Wait for workflow to start
            
            runs = workflow.get_runs()
            latest_run = runs[0] if runs.totalCount > 0 else None
            
            return {
                'success': True,
                'workflow_name': workflow.name,
                'run_id': latest_run.id if latest_run else None,
                'run_url': latest_run.html_url if latest_run else None
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error triggering process workflow: {error_msg}")
            
            # Provide helpful error message for common issues
            if '404' in error_msg:
                raise Exception(
                    f"Workflow file '{workflow_file}' not found in repository. "
                    "Please ensure you have committed and pushed the .github/workflows/ file to GitHub. "
                    f"Run: git add .github/workflows/{workflow_file} && git commit -m 'Add workflow' && git push"
                )
            else:
                raise
    
    def check_and_download_artifact(self, run_id, artifact_name='process-report'):
        """
        Check for workflow artifacts and download if available.
        
        Args:
            run_id: GitHub Actions workflow run ID
            artifact_name: Name of the artifact to download
        
        Returns:
            Dictionary with status and download information
        """
        if not self.repo:
            logger.error("No repository connected")
            return {'success': False, 'error': 'GitHub repository not connected'}
        
        try:
            import os
            import requests
            import zipfile
            import io
            
            # Get the workflow run
            run = self.repo.get_workflow_run(run_id)
            
            # Check run status
            if run.status != 'completed':
                return {
                    'success': False,
                    'status': run.status,
                    'message': f'Workflow is {run.status}. Please wait for completion.'
                }
            
            # Check if run was successful
            if run.conclusion != 'success':
                return {
                    'success': False,
                    'status': run.status,
                    'conclusion': run.conclusion,
                    'message': f'Workflow {run.conclusion}. No artifact available.'
                }
            
            # Get artifacts
            artifacts = run.get_artifacts()
            
            target_artifact = None
            for artifact in artifacts:
                if artifact.name == artifact_name:
                    target_artifact = artifact
                    break
            
            if not target_artifact:
                return {
                    'success': False,
                    'message': f'Artifact "{artifact_name}" not found in workflow run.'
                }
            
            # Download artifact
            # Note: PyGithub doesn't directly support artifact download, need to use API
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            download_url = target_artifact.archive_download_url
            response = requests.get(download_url, headers=headers)
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'message': f'Failed to download artifact: HTTP {response.status_code}'
                }
            
            # Extract zip file
            os.makedirs('generated_reports', exist_ok=True)
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                # Extract all files from the artifact
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith('.docx'):
                        # Extract to generated_reports folder
                        zip_ref.extract(file_info.filename, 'generated_reports')
                        extracted_filename = file_info.filename
                        
                        logger.info(f"Downloaded artifact: {extracted_filename}")
                        
                        return {
                            'success': True,
                            'status': 'completed',
                            'filename': extracted_filename,
                            'download_url': f'/api/download/{extracted_filename}',
                            'message': 'Artifact downloaded successfully'
                        }
            
            return {
                'success': False,
                'message': 'No .docx file found in artifact'
            }
            
        except Exception as e:
            logger.error(f"Error checking/downloading artifact: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # Backward compatibility alias
    def trigger_sox_workflow(self, control_name, control_data, analysis_type='standard'):
        """Legacy function for backward compatibility. Calls trigger_process_workflow."""
        return self.trigger_process_workflow(control_name, control_data, analysis_type, 'sox-analysis-doc.yml')
