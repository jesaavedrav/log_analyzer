# Log Analyzer - CORE_MS Project

This project provides a visualization tool for analyzing log patterns from the CORE_MS project.

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone this repository or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To generate analysis charts, simply run:

```bash
python main.py
```

This command will generate three interactive HTML visualizations:

1. `error_distribution.html` - Shows the distribution of errors by category in a donut chart
2. `severity_comparison.html` - Compares the number of messages by severity level (ERROR vs WARNING)
3. `category_analysis.html` - Provides a detailed analysis by category and severity using a treemap

## Visualizations

### 1. Error Distribution
- Donut chart showing the proportion of errors in each category (Connection, File, Control)

### 2. Severity Comparison
- Bar chart comparing the number of ERROR vs WARNING messages

### 3. Detailed Analysis
- Interactive treemap showing the complete hierarchy of messages, categories, and severities

## Notes
- Visualizations are interactive and can be explored in any modern web browser
- Charts use an intuitive color palette to differentiate between severity types
- You can hover over elements to see more details 