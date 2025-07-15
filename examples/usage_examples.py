#!/usr/bin/env python3
"""
Comprehensive Usage Examples for Jagarnath Python APIs

This file demonstrates how to use all the Python APIs including:
- DataProcessor: Data loading, cleaning, transformation, and analysis
- MLUtils: Machine learning model training, evaluation, and optimization
- WebScraper: Web scraping with rate limiting and data extraction
- FileUtils: File operations, compression, and format conversion

@author: Jagarnath Team
@version: 1.0.0
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

# Import our custom modules
from src.python.data_processor import DataProcessor
from src.python.ml_utils import MLUtils
from src.python.web_scraper import WebScraper
from src.python.file_utils import FileUtils


def data_processing_examples():
    """Demonstrate DataProcessor functionality"""
    print("=== Data Processing Examples ===\n")
    
    # Initialize DataProcessor
    processor = DataProcessor()
    
    # Example 1: Load and clean data
    print("1. Loading and cleaning sample data...")
    
    # Create sample data
    sample_data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 75000, 55000, 70000],
        'department': ['IT', 'HR', 'IT', 'Finance', 'Marketing'],
        'hire_date': ['2020-01-15', '2019-03-20', '2018-07-10', '2021-02-28', '2017-11-05']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Save sample data
    processor.save_data(df, 'sample_employees.csv')
    
    # Load data
    loaded_data = processor.load_data('sample_employees.csv')
    print(f"Loaded {len(loaded_data)} records")
    
    # Clean data
    cleaned_data = processor.clean_data(loaded_data)
    print(f"Cleaned data shape: {cleaned_data.shape}")
    
    # Example 2: Data transformation
    print("\n2. Transforming data...")
    
    # Add calculated columns
    transformations = {
        'salary_category': lambda x: np.where(x['salary'] > 65000, 'High', 'Medium'),
        'years_employed': lambda x: (datetime.now().year - pd.to_datetime(x['hire_date']).dt.year),
        'age_group': lambda x: np.where(x['age'] < 30, 'Young', 
                                       np.where(x['age'] < 40, 'Middle', 'Senior'))
    }
    
    transformed_data = processor.transform_data(cleaned_data, transformations)
    print("Added columns: salary_category, years_employed, age_group")
    
    # Example 3: Data analysis
    print("\n3. Analyzing data...")
    
    # Get statistics
    stats = processor.get_statistics(transformed_data)
    print("Data statistics:")
    print(json.dumps(stats, indent=2))
    
    # Group by analysis
    dept_stats = processor.group_by_analysis(transformed_data, 'department', ['salary', 'age'])
    print("\nDepartment statistics:")
    print(dept_stats)
    
    # Example 4: Export data
    print("\n4. Exporting data...")
    
    # Export to different formats
    processor.export_data(transformed_data, 'employees_processed.xlsx')
    processor.export_data(transformed_data, 'employees_processed.json')
    print("Data exported to Excel and JSON formats")


def machine_learning_examples():
    """Demonstrate MLUtils functionality"""
    print("\n=== Machine Learning Examples ===\n")
    
    # Initialize MLUtils
    ml_utils = MLUtils()
    
    # Example 1: Prepare sample data
    print("1. Preparing sample dataset...")
    
    # Create synthetic data for classification
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    X = np.random.randn(n_samples, 4)
    X[:, 0] = X[:, 0] * 2 + 1  # Feature 1
    X[:, 1] = X[:, 1] * 1.5 - 0.5  # Feature 2
    X[:, 2] = X[:, 2] * 0.8 + 2  # Feature 3
    X[:, 3] = X[:, 3] * 1.2 - 1  # Feature 4
    
    # Target (binary classification)
    y = (X[:, 0] + X[:, 1] * 2 + X[:, 2] * 0.5 + X[:, 3] * 1.5 + np.random.randn(n_samples) * 0.1 > 0).astype(int)
    
    feature_names = ['feature_1', 'feature_2', 'feature_3', 'feature_4']
    
    # Example 2: Train a model
    print("2. Training classification model...")
    
    # Train model
    model, metrics = ml_utils.train_model(
        X, y, 
        model_type='classification',
        test_size=0.2,
        random_state=42
    )
    
    print("Training completed!")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
    
    # Example 3: Hyperparameter tuning
    print("\n3. Performing hyperparameter tuning...")
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, None],
        'min_samples_split': [2, 5, 10]
    }
    
    best_params, best_score = ml_utils.hyperparameter_tuning(
        X, y,
        model_type='classification',
        param_grid=param_grid,
        cv=3,
        n_jobs=-1
    )
    
    print(f"Best parameters: {best_params}")
    print(f"Best cross-validation score: {best_score:.4f}")
    
    # Example 4: Feature importance
    print("\n4. Analyzing feature importance...")
    
    importance = ml_utils.get_feature_importance(model, feature_names)
    print("Feature importance:")
    for feature, imp in importance.items():
        print(f"  {feature}: {imp:.4f}")
    
    # Example 5: Save and load model
    print("\n5. Saving and loading model...")
    
    # Save model
    ml_utils.save_model(model, 'classification_model.pkl')
    print("Model saved successfully")
    
    # Load model
    loaded_model = ml_utils.load_model('classification_model.pkl')
    print("Model loaded successfully")
    
    # Test loaded model
    test_prediction = loaded_model.predict(X[:5])
    print(f"Test predictions: {test_prediction}")


def web_scraping_examples():
    """Demonstrate WebScraper functionality"""
    print("\n=== Web Scraping Examples ===\n")
    
    # Initialize WebScraper
    scraper = WebScraper()
    
    # Example 1: Scrape a simple webpage
    print("1. Scraping webpage content...")
    
    try:
        # Scrape a public API documentation page
        url = "https://httpbin.org/json"
        content = scraper.scrape_website(url)
        
        if content:
            print(f"Successfully scraped {len(content)} characters from {url}")
            print("First 200 characters:")
            print(content[:200] + "...")
        else:
            print("Failed to scrape content")
            
    except Exception as e:
        print(f"Error scraping website: {e}")
    
    # Example 2: Scrape articles
    print("\n2. Scraping articles...")
    
    try:
        # This would normally be a real news site
        # For demo purposes, we'll use a mock example
        articles = scraper.scrape_articles("https://example.com/news")
        print(f"Found {len(articles)} articles")
        
        if articles:
            for i, article in enumerate(articles[:3], 1):
                print(f"Article {i}: {article.get('title', 'No title')}")
                print(f"  URL: {article.get('url', 'No URL')}")
                print(f"  Summary: {article.get('summary', 'No summary')[:100]}...")
                print()
                
    except Exception as e:
        print(f"Error scraping articles: {e}")
    
    # Example 3: Scrape tables
    print("3. Scraping tables...")
    
    try:
        # Scrape tables from a webpage
        tables = scraper.scrape_tables("https://example.com/data")
        print(f"Found {len(tables)} tables")
        
        if tables:
            for i, table in enumerate(tables[:2], 1):
                print(f"Table {i} shape: {table.shape}")
                print("First few rows:")
                print(table.head())
                print()
                
    except Exception as e:
        print(f"Error scraping tables: {e}")
    
    # Example 4: API data extraction
    print("4. Extracting data from APIs...")
    
    try:
        # Extract data from a public API
        api_url = "https://jsonplaceholder.typicode.com/posts"
        api_data = scraper.extract_api_data(api_url)
        
        if api_data:
            print(f"Extracted {len(api_data)} posts from API")
            print("Sample post:")
            print(json.dumps(api_data[0], indent=2))
            
    except Exception as e:
        print(f"Error extracting API data: {e}")
    
    # Example 5: Export scraped data
    print("\n5. Exporting scraped data...")
    
    # Create sample scraped data
    sample_data = {
        'articles': [
            {'title': 'Sample Article 1', 'url': 'https://example.com/1', 'content': 'Sample content...'},
            {'title': 'Sample Article 2', 'url': 'https://example.com/2', 'content': 'Sample content...'}
        ],
        'tables': [pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})]
    }
    
    # Export to different formats
    scraper.export_data(sample_data, 'scraped_data.json')
    print("Scraped data exported to JSON")


def file_operations_examples():
    """Demonstrate FileUtils functionality"""
    print("\n=== File Operations Examples ===\n")
    
    # Initialize FileUtils
    file_utils = FileUtils()
    
    # Example 1: Read and write different file formats
    print("1. Reading and writing different file formats...")
    
    # Create sample data
    sample_data = {
        'users': [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'},
            {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com'}
        ]
    }
    
    # Write to different formats
    file_utils.write_json(sample_data, 'users.json')
    file_utils.write_csv(pd.DataFrame(sample_data['users']), 'users.csv')
    file_utils.write_excel(pd.DataFrame(sample_data['users']), 'users.xlsx')
    
    print("Data written to JSON, CSV, and Excel formats")
    
    # Read from different formats
    json_data = file_utils.read_json('users.json')
    csv_data = file_utils.read_csv('users.csv')
    excel_data = file_utils.read_excel('users.xlsx')
    
    print(f"JSON data: {len(json_data['users'])} users")
    print(f"CSV data: {len(csv_data)} rows")
    print(f"Excel data: {len(excel_data)} rows")
    
    # Example 2: Directory operations
    print("\n2. Directory operations...")
    
    # Create directory
    file_utils.create_directory('example_dir')
    print("Created directory: example_dir")
    
    # List directory contents
    contents = file_utils.list_directory('.')
    print(f"Current directory has {len(contents)} items")
    
    # Check if file exists
    exists = file_utils.file_exists('users.json')
    print(f"users.json exists: {exists}")
    
    # Example 3: File compression
    print("\n3. File compression...")
    
    # Compress files
    files_to_compress = ['users.json', 'users.csv', 'users.xlsx']
    file_utils.compress_files(files_to_compress, 'users_archive.zip')
    print("Files compressed to users_archive.zip")
    
    # Extract files
    file_utils.extract_archive('users_archive.zip', 'extracted_files')
    print("Files extracted to extracted_files directory")
    
    # Example 4: File information
    print("\n4. File information...")
    
    # Get file info
    file_info = file_utils.get_file_info('users.json')
    print("File information:")
    print(f"  Size: {file_info['size']} bytes")
    print(f"  Created: {file_info['created']}")
    print(f"  Modified: {file_info['modified']}")
    print(f"  Type: {file_info['type']}")
    
    # Example 5: File search
    print("\n5. File search...")
    
    # Search for files
    json_files = file_utils.search_files('.', '*.json')
    print(f"Found {len(json_files)} JSON files:")
    for file in json_files:
        print(f"  - {file}")


def main():
    """Run all examples"""
    print("Jagarnath Python API Examples")
    print("=" * 50)
    
    try:
        # Run all examples
        data_processing_examples()
        machine_learning_examples()
        web_scraping_examples()
        file_operations_examples()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()