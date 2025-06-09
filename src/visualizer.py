"""
Visualization module for log analyzer.
Contains all plotting functions and visualization logic.
"""
from typing import Dict, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from src.config import Config

class LogVisualizer:
    """Class for creating visualizations of log data."""
    
    def __init__(self, config: Config):
        """
        Initialize visualizer with configuration.
        
        Args:
            config: Configuration object containing visualization settings.
        """
        self.config = config
        self.processed_error_logs = self._preprocess_logs(config.error_logs)
        self.processed_warning_logs = self._preprocess_logs(config.warning_logs)
    
    @staticmethod
    def _preprocess_logs(logs: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Preprocess log messages to remove variable parts.
        
        Args:
            logs: Dictionary of log messages by category.
            
        Returns:
            Dictionary of preprocessed log messages.
        """
        return {
            cat: [msg.split('{')[0].strip() for msg in msgs]
            for cat, msgs in logs.items()
        }
    
    def _save_figure(self, fig: go.Figure, name: str) -> None:
        """
        Save figure in configured formats.
        
        Args:
            fig: Plotly figure object.
            name: Base name for the output file.
        """
        if self.config.output.save_plots:
            for fmt in self.config.output.formats:
                output_path = Path(self.config.output.output_dir) / f"{name}.{fmt}"
                if fmt == 'html':
                    fig.write_html(str(output_path))
                elif fmt == 'png':
                    fig.write_image(str(output_path))
    
    def create_error_distribution(self) -> None:
        """Create and display error distribution chart."""
        error_counts = {
            category: len(messages)
            for category, messages in self.processed_error_logs.items()
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(error_counts.keys()),
            values=list(error_counts.values()),
            hole=.3
        )])
        
        fig.update_layout(
            title=self.config.visualization.titles['error_distribution'],
            annotations=[dict(
                text='Errors',
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False
            )]
        )
        
        self._save_figure(fig, 'error_distribution')
        fig.show()
    
    def create_severity_comparison(self) -> None:
        """Create and display severity comparison chart."""
        error_total = sum(len(msgs) for msgs in self.processed_error_logs.values())
        warning_total = sum(len(msgs) for msgs in self.processed_warning_logs.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=['ERROR', 'WARNING'],
                y=[error_total, warning_total],
                text=[error_total, warning_total],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=self.config.visualization.titles['severity_comparison'],
            xaxis_title=self.config.visualization.labels['severity'],
            yaxis_title=self.config.visualization.labels['message_count'],
            template='plotly_white'
        )
        
        self._save_figure(fig, 'severity_comparison')
        fig.show()
    
    def create_detailed_analysis(self) -> None:
        """Create and display detailed category analysis."""
        df = self._prepare_detailed_analysis_data()
        
        fig = px.treemap(
            df,
            path=[px.Constant("All Messages"), 'Severity', 'Category'],
            values='Count',
            color='Severity',
            color_discrete_map={
                'ERROR': self.config.visualization.colors['error'],
                'WARNING': self.config.visualization.colors['warning']
            }
        )
        
        fig.update_layout(
            title=self.config.visualization.titles['detailed_analysis']
        )
        
        self._save_figure(fig, 'detailed_analysis')
        fig.show()
    
    def _prepare_detailed_analysis_data(self) -> pd.DataFrame:
        """
        Prepare data for detailed analysis visualization.
        
        Returns:
            DataFrame containing prepared data.
        """
        data = []
        
        # Process error logs
        for category, messages in self.processed_error_logs.items():
            data.append({
                'Category': category,
                'Count': len(messages),
                'Severity': 'ERROR'
            })
        
        # Process warning logs
        for category, messages in self.processed_warning_logs.items():
            data.append({
                'Category': category,
                'Count': len(messages),
                'Severity': 'WARNING'
            })
        
        return pd.DataFrame(data)
    
    def create_error_histogram(self) -> None:
        """Create and display error message histogram."""
        messages = []
        for msgs in self.processed_error_logs.values():
            messages.extend(msgs)
        
        df = pd.DataFrame({'Message': messages})
        fig = px.histogram(
            df,
            x='Message',
            color_discrete_sequence=[self.config.visualization.colors['error']]
        )
        
        fig.update_layout(
            title=self.config.visualization.titles['error_histogram'],
            xaxis_title=self.config.visualization.labels['error_message'],
            yaxis_title=self.config.visualization.labels['frequency']
        )
        
        self._save_figure(fig, 'error_histogram')
        fig.show()
    
    def create_warning_histogram(self) -> None:
        """Create and display warning message histogram."""
        messages = []
        for msgs in self.processed_warning_logs.values():
            messages.extend(msgs)
        
        df = pd.DataFrame({'Message': messages})
        fig = px.histogram(
            df,
            x='Message',
            color_discrete_sequence=[self.config.visualization.colors['warning']]
        )
        
        fig.update_layout(
            title=self.config.visualization.titles['warning_histogram'],
            xaxis_title=self.config.visualization.labels['warning_message'],
            yaxis_title=self.config.visualization.labels['frequency']
        )
        
        self._save_figure(fig, 'warning_histogram')
        fig.show() 