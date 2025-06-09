"""
Main script for log analyzer.
"""
import argparse
from pathlib import Path
from src.config import load_config, ensure_output_dir
from src.visualizer import LogVisualizer

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Analyze and visualize log patterns from CORE_MS project.'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.json',
        help='Path to configuration file'
    )
    return parser.parse_args()

def main():
    """Main function."""
    # Parse command line arguments
    args = parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Ensure output directory exists
        ensure_output_dir(config)
        
        # Create visualizer
        visualizer = LogVisualizer(config)
        
        # Create all visualizations
        print("Generating visualizations...")
        visualizer.create_error_distribution()
        visualizer.create_severity_comparison()
        visualizer.create_detailed_analysis()
        visualizer.create_error_histogram()
        visualizer.create_warning_histogram()
        
        # Print completion message
        print("\nAnalysis completed successfully!")
        if config.output.save_plots:
            print(f"\nGraphs have been saved in: {config.output.output_dir}")
            print(f"Generated formats: {', '.join(config.output.formats)}")
        
        print("\nGenerated visualizations:")
        print("1. Error distribution by category")
        print("2. Message comparison by severity level")
        print("3. Detailed analysis by category and severity")
        print("4. Error message frequency histogram")
        print("5. Warning message frequency histogram")
        
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 