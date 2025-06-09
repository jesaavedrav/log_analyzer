"""
Configuration module for log analyzer.
Handles loading and validating configuration from JSON files.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from typing import List

@dataclass
class VisualizationConfig:
    """Configuration for visualization settings."""
    colors: Dict[str, str]
    titles: Dict[str, str]
    labels: Dict[str, str]

@dataclass
class OutputConfig:
    """Configuration for output settings."""
    save_plots: bool
    output_dir: str
    formats: List[str]

@dataclass
class Config:
    """Main configuration class."""
    log_patterns_file: str
    visualization: VisualizationConfig
    output: OutputConfig
    error_logs: Optional[Dict[str, List[str]]] = None
    warning_logs: Optional[Dict[str, List[str]]] = None

def load_config(config_path: str = "config/config.json") -> Config:
    """
    Load configuration from JSON files.
    
    Args:
        config_path: Path to the main configuration file.
        
    Returns:
        Config object containing all configuration settings.
    
    Raises:
        FileNotFoundError: If configuration files are not found.
        json.JSONDecodeError: If configuration files are invalid JSON.
    """
    # Ensure config directory exists
    config_dir = Path(config_path).parent
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    
    # Load main config
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    # Load log patterns
    log_patterns_path = config_data['log_patterns_file']
    with open(log_patterns_path, 'r', encoding='utf-8') as f:
        log_patterns = json.load(f)
    
    # Create config object
    config = Config(
        log_patterns_file=log_patterns_path,
        visualization=VisualizationConfig(**config_data['visualization']),
        output=OutputConfig(**config_data['output']),
        error_logs=log_patterns['error_logs'],
        warning_logs=log_patterns['warning_logs']
    )
    
    return config

def ensure_output_dir(config: Config) -> None:
    """
    Ensure output directory exists.
    
    Args:
        config: Configuration object containing output settings.
    """
    output_dir = Path(config.output.output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True) 