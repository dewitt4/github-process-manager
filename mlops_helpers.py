"""
MLOps Helper Functions - Isolated Module
This module provides utilities for ML metrics parsing and formatting.
Only imported when MLOps features are explicitly used.
"""
import json
from typing import Dict, List, Optional, Union
from logger import logger


def parse_ml_metrics(metrics_json: Union[str, Dict]) -> Dict:
    """
    Parse ML metrics from JSON string or dict - standalone function.
    No dependencies on app.py, gemini_client, or github_client.
    
    Args:
        metrics_json: JSON string or dict containing ML metrics
        
    Returns:
        Dict with standardized metric names and values
        
    Example:
        >>> parse_ml_metrics('{"accuracy": 0.95, "f1_score": 0.93}')
        {'accuracy': 0.95, 'f1_score': 0.93, 'precision': 'N/A', 'recall': 'N/A', 'loss': 'N/A'}
    """
    try:
        # Convert string to dict if needed
        if isinstance(metrics_json, str):
            metrics = json.loads(metrics_json)
        elif isinstance(metrics_json, dict):
            metrics = metrics_json
        else:
            logger.warning(f"Invalid metrics type: {type(metrics_json)}")
            return _get_default_metrics()
        
        # Standardize metric names and extract values
        standardized = {
            'accuracy': _get_metric(metrics, ['accuracy', 'acc', 'accuracy_score']),
            'precision': _get_metric(metrics, ['precision', 'prec', 'precision_score']),
            'recall': _get_metric(metrics, ['recall', 'rec', 'recall_score', 'sensitivity']),
            'f1_score': _get_metric(metrics, ['f1_score', 'f1', 'f1-score']),
            'auc_roc': _get_metric(metrics, ['auc_roc', 'auc', 'roc_auc', 'auc_score']),
            'loss': _get_metric(metrics, ['loss', 'training_loss', 'val_loss']),
            'mae': _get_metric(metrics, ['mae', 'mean_absolute_error']),
            'rmse': _get_metric(metrics, ['rmse', 'root_mean_squared_error']),
            'r2_score': _get_metric(metrics, ['r2_score', 'r2', 'r_squared']),
        }
        
        # Add any custom metrics not in the standard set
        for key, value in metrics.items():
            standardized_key = key.lower().replace('-', '_').replace(' ', '_')
            if standardized_key not in standardized:
                standardized[standardized_key] = value
        
        logger.info(f"Parsed {len(standardized)} metrics from input")
        return standardized
        
    except (json.JSONDecodeError, AttributeError, TypeError) as e:
        logger.error(f"Error parsing metrics JSON: {e}")
        return _get_default_metrics()


def _get_metric(metrics: Dict, possible_keys: List[str]) -> Union[float, str]:
    """
    Get metric value from dict using multiple possible key names.
    
    Args:
        metrics: Dictionary of metrics
        possible_keys: List of possible key names to check
        
    Returns:
        Metric value or 'N/A' if not found
    """
    for key in possible_keys:
        if key in metrics:
            return metrics[key]
        # Try case-insensitive match
        for k, v in metrics.items():
            if k.lower() == key.lower():
                return v
    return 'N/A'


def _get_default_metrics() -> Dict:
    """Return default metrics structure with N/A values."""
    return {
        'accuracy': 'N/A',
        'precision': 'N/A',
        'recall': 'N/A',
        'f1_score': 'N/A',
        'auc_roc': 'N/A',
        'loss': 'N/A',
        'mae': 'N/A',
        'rmse': 'N/A',
        'r2_score': 'N/A',
    }


def format_ml_metrics_for_document(metrics: Dict) -> str:
    """
    Convert metrics dict to formatted string for Word documents.
    Standalone - no external dependencies.
    
    Args:
        metrics: Dictionary of metric names and values
        
    Returns:
        Formatted string for document insertion
        
    Example:
        >>> metrics = {'accuracy': 0.95, 'f1_score': 0.93}
        >>> print(format_ml_metrics_for_document(metrics))
        **Model Performance Metrics:**
        
        • Accuracy: 0.9500
        • F1 Score: 0.9300
    """
    if not metrics:
        return "**Model Performance Metrics:**\n\nNo metrics provided."
    
    lines = ["**Model Performance Metrics:**\n"]
    
    # Order metrics for better readability
    metric_order = [
        'accuracy', 'precision', 'recall', 'f1_score', 'auc_roc',
        'loss', 'mae', 'rmse', 'r2_score'
    ]
    
    # Add ordered metrics first
    for key in metric_order:
        if key in metrics and metrics[key] != 'N/A':
            value = metrics[key]
            label = key.replace('_', ' ').title()
            if isinstance(value, (int, float)):
                lines.append(f"• {label}: {value:.4f}")
            else:
                lines.append(f"• {label}: {value}")
    
    # Add any custom metrics not in the ordered list
    for key, value in metrics.items():
        if key not in metric_order:
            label = key.replace('_', ' ').title()
            if isinstance(value, (int, float)):
                lines.append(f"• {label}: {value:.4f}")
            else:
                lines.append(f"• {label}: {value}")
    
    return '\n'.join(lines)


def validate_metrics_schema(metrics: Dict, required_metrics: Optional[List[str]] = None) -> tuple[bool, List[str]]:
    """
    Validate that metrics dict contains required fields.
    
    Args:
        metrics: Dictionary of metrics
        required_metrics: List of required metric names (optional)
        
    Returns:
        Tuple of (is_valid, list_of_missing_metrics)
        
    Example:
        >>> metrics = {'accuracy': 0.95}
        >>> valid, missing = validate_metrics_schema(metrics, ['accuracy', 'f1_score'])
        >>> print(valid, missing)
        False ['f1_score']
    """
    if required_metrics is None:
        # Default required metrics for classification
        required_metrics = ['accuracy']
    
    missing = []
    for metric in required_metrics:
        if metric not in metrics or metrics[metric] == 'N/A':
            missing.append(metric)
    
    is_valid = len(missing) == 0
    return is_valid, missing


def calculate_model_score(metrics: Dict, weights: Optional[Dict[str, float]] = None) -> float:
    """
    Calculate weighted model score from multiple metrics.
    
    Args:
        metrics: Dictionary of metric values
        weights: Optional dict of metric weights (must sum to 1.0)
        
    Returns:
        Weighted score between 0 and 1, or 0.0 if calculation fails
        
    Example:
        >>> metrics = {'accuracy': 0.95, 'f1_score': 0.93}
        >>> weights = {'accuracy': 0.5, 'f1_score': 0.5}
        >>> score = calculate_model_score(metrics, weights)
        >>> print(score)
        0.94
    """
    if weights is None:
        # Default equal weights for available metrics
        weights = {'accuracy': 0.4, 'precision': 0.2, 'recall': 0.2, 'f1_score': 0.2}
    
    try:
        score = 0.0
        total_weight = 0.0
        
        for metric_name, weight in weights.items():
            if metric_name in metrics and metrics[metric_name] != 'N/A':
                value = float(metrics[metric_name])
                score += value * weight
                total_weight += weight
        
        # Normalize by actual total weight used
        if total_weight > 0:
            return score / total_weight
        else:
            return 0.0
            
    except (ValueError, TypeError) as e:
        logger.error(f"Error calculating model score: {e}")
        return 0.0


def get_metrics_summary(metrics: Dict) -> str:
    """
    Generate a human-readable summary of model metrics.
    
    Args:
        metrics: Dictionary of metrics
        
    Returns:
        Summary string describing model performance
    """
    if not metrics or all(v == 'N/A' for v in metrics.values()):
        return "No performance metrics available."
    
    summary_parts = []
    
    # Check accuracy
    if 'accuracy' in metrics and metrics['accuracy'] != 'N/A':
        acc = float(metrics['accuracy'])
        if acc >= 0.95:
            summary_parts.append(f"Excellent accuracy ({acc:.2%})")
        elif acc >= 0.90:
            summary_parts.append(f"Good accuracy ({acc:.2%})")
        elif acc >= 0.85:
            summary_parts.append(f"Acceptable accuracy ({acc:.2%})")
        else:
            summary_parts.append(f"Low accuracy ({acc:.2%})")
    
    # Check F1 score
    if 'f1_score' in metrics and metrics['f1_score'] != 'N/A':
        f1 = float(metrics['f1_score'])
        if f1 >= 0.90:
            summary_parts.append(f"strong F1 score ({f1:.3f})")
        elif f1 >= 0.80:
            summary_parts.append(f"moderate F1 score ({f1:.3f})")
    
    # Check precision and recall balance
    if ('precision' in metrics and metrics['precision'] != 'N/A' and
        'recall' in metrics and metrics['recall'] != 'N/A'):
        prec = float(metrics['precision'])
        rec = float(metrics['recall'])
        diff = abs(prec - rec)
        if diff < 0.05:
            summary_parts.append("well-balanced precision and recall")
        elif prec > rec:
            summary_parts.append(f"higher precision ({prec:.2%}) than recall ({rec:.2%})")
        else:
            summary_parts.append(f"higher recall ({rec:.2%}) than precision ({prec:.2%})")
    
    if summary_parts:
        return "Model shows " + ", ".join(summary_parts) + "."
    else:
        return "Model performance metrics available."


def export_metrics_to_mlflow_format(metrics: Dict, run_name: str = "model_run") -> Dict:
    """
    Convert metrics to MLflow-compatible format.
    
    Args:
        metrics: Dictionary of metrics
        run_name: Name for the MLflow run
        
    Returns:
        Dict in MLflow format
    """
    mlflow_metrics = {
        "run_name": run_name,
        "metrics": {},
        "params": {},
        "tags": {}
    }
    
    # Convert metrics to MLflow format
    for key, value in metrics.items():
        if value != 'N/A' and isinstance(value, (int, float)):
            mlflow_metrics["metrics"][f"metrics.{key}"] = float(value)
    
    return mlflow_metrics


# NO imports from app.py, gemini_client, github_client, rag_engine
# NO modifications to existing code required
# Optional: only loaded if MLOps features are used
