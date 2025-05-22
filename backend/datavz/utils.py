import pandas as pd
import numpy as np
import json

def process_excel_file(file_path):
    """Process an Excel file and return basic statistics"""
    try:
        df = pd.read_excel(file_path)
        stats = {
            'columns': df.columns.tolist(),
            'rows': len(df),
            'numerical_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'sample': df.head(5).to_dict(orient='records')
        }
        return stats
    except Exception as e:
        raise Exception(f"Error processing Excel file: {str(e)}")

def generate_visualization_config(chart_type, columns):
    """Generate a default visualization configuration based on chart type and available columns"""
    config = {}
    
    numerical_columns = [col for col in columns if col.get('type') == 'number']
    categorical_columns = [col for col in columns if col.get('type') == 'string']
    
    if chart_type == 'bar':
        if categorical_columns and numerical_columns:
            config = {
                'x_column': categorical_columns[0]['name'],
                'y_column': numerical_columns[0]['name']
            }
    
    elif chart_type == 'line':
        if categorical_columns and numerical_columns:
            config = {
                'x_column': categorical_columns[0]['name'],
                'y_columns': [col['name'] for col in numerical_columns[:3]]
            }
    
    elif chart_type == 'pie':
        if categorical_columns and numerical_columns:
            config = {
                'labels': categorical_columns[0]['name'],
                'values': numerical_columns[0]['name']
            }
    
    elif chart_type == 'scatter':
        if len(numerical_columns) >= 2:
            config = {
                'x_column': numerical_columns[0]['name'],
                'y_column': numerical_columns[1]['name']
            }
    
    return config