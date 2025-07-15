#!/usr/bin/env python3
"""
Comprehensive Test Examples for Jagarnath Python APIs

This file demonstrates how to test all the Python APIs including:
- DataProcessor: Data loading, cleaning, transformation, and analysis
- MLUtils: Machine learning model training, evaluation, and optimization
- WebScraper: Web scraping with rate limiting and data extraction
- FileUtils: File operations, compression, and format conversion

@author: Jagarnath Team
@version: 1.0.0
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import our custom modules
from src.python.data_processor import DataProcessor
from src.python.ml_utils import MLUtils
from src.python.web_scraper import WebScraper
from src.python.file_utils import FileUtils


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.sample_data = pd.DataFrame({
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 75000],
            'department': ['IT', 'HR', 'IT'],
            'hire_date': ['2020-01-15', '2019-03-20', '2018-07-10']
        })
    
    def test_load_data_csv(self):
        """Test loading CSV data"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.sample_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            # Test loading
            loaded_data = self.processor.load_data(temp_file)
            self.assertIsInstance(loaded_data, pd.DataFrame)
            self.assertEqual(len(loaded_data), 3)
            self.assertEqual(list(loaded_data.columns), list(self.sample_data.columns))
        finally:
            os.unlink(temp_file)
    
    def test_clean_data(self):
        """Test data cleaning functionality"""
        # Add some dirty data
        dirty_data = self.sample_data.copy()
        dirty_data.loc[0, 'age'] = np.nan
        dirty_data.loc[1, 'salary'] = -1000
        dirty_data.loc[2, 'name'] = ''
        
        # Clean data
        cleaned_data = self.processor.clean_data(dirty_data)
        
        # Assertions
        self.assertIsInstance(cleaned_data, pd.DataFrame)
        self.assertEqual(len(cleaned_data), 1)  # Only one valid row should remain
        self.assertFalse(cleaned_data['age'].isna().any())
        self.assertTrue((cleaned_data['salary'] > 0).all())
    
    def test_transform_data(self):
        """Test data transformation functionality"""
        transformations = {
            'salary_category': lambda x: np.where(x['salary'] > 65000, 'High', 'Medium'),
            'years_employed': lambda x: (datetime.now().year - pd.to_datetime(x['hire_date']).dt.year)
        }
        
        transformed_data = self.processor.transform_data(self.sample_data, transformations)
        
        # Assertions
        self.assertIn('salary_category', transformed_data.columns)
        self.assertIn('years_employed', transformed_data.columns)
        self.assertEqual(len(transformed_data), 3)
        
        # Check salary categories
        high_salary_count = (transformed_data['salary_category'] == 'High').sum()
        self.assertEqual(high_salary_count, 1)  # Only one salary > 65000
    
    def test_get_statistics(self):
        """Test statistics calculation"""
        stats = self.processor.get_statistics(self.sample_data)
        
        # Assertions
        self.assertIsInstance(stats, dict)
        self.assertIn('summary', stats)
        self.assertIn('missing_values', stats)
        self.assertIn('data_types', stats)
        
        # Check specific statistics
        self.assertEqual(stats['summary']['age']['mean'], 30.0)
        self.assertEqual(stats['summary']['salary']['mean'], 61666.67)
    
    def test_group_by_analysis(self):
        """Test group by analysis"""
        result = self.processor.group_by_analysis(
            self.sample_data, 
            'department', 
            ['salary', 'age']
        )
        
        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn('IT', result)
        self.assertIn('HR', result)
        
        # Check IT department stats
        it_stats = result['IT']
        self.assertEqual(it_stats['salary']['count'], 2)
        self.assertEqual(it_stats['age']['count'], 2)


class TestMLUtils(unittest.TestCase):
    """Test cases for MLUtils class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ml_utils = MLUtils()
        
        # Create synthetic data
        np.random.seed(42)
        self.X = np.random.randn(100, 3)
        self.y = (self.X[:, 0] + self.X[:, 1] * 2 + np.random.randn(100) * 0.1 > 0).astype(int)
        self.feature_names = ['feature_1', 'feature_2', 'feature_3']
    
    def test_train_model_classification(self):
        """Test model training for classification"""
        model, metrics = self.ml_utils.train_model(
            self.X, self.y,
            model_type='classification',
            test_size=0.2,
            random_state=42
        )
        
        # Assertions
        self.assertIsNotNone(model)
        self.assertIsInstance(metrics, dict)
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1_score', metrics)
        
        # Check metric ranges
        self.assertGreaterEqual(metrics['accuracy'], 0.0)
        self.assertLessEqual(metrics['accuracy'], 1.0)
        self.assertGreaterEqual(metrics['precision'], 0.0)
        self.assertLessEqual(metrics['precision'], 1.0)
    
    def test_train_model_regression(self):
        """Test model training for regression"""
        # Create regression target
        y_reg = self.X[:, 0] + self.X[:, 1] * 2 + np.random.randn(100) * 0.1
        
        model, metrics = self.ml_utils.train_model(
            self.X, y_reg,
            model_type='regression',
            test_size=0.2,
            random_state=42
        )
        
        # Assertions
        self.assertIsNotNone(model)
        self.assertIsInstance(metrics, dict)
        self.assertIn('r2_score', metrics)
        self.assertIn('mean_squared_error', metrics)
        self.assertIn('mean_absolute_error', metrics)
    
    def test_hyperparameter_tuning(self):
        """Test hyperparameter tuning"""
        param_grid = {
            'n_estimators': [10, 20],
            'max_depth': [3, 5]
        }
        
        best_params, best_score = self.ml_utils.hyperparameter_tuning(
            self.X, self.y,
            model_type='classification',
            param_grid=param_grid,
            cv=2,
            n_jobs=1
        )
        
        # Assertions
        self.assertIsInstance(best_params, dict)
        self.assertIsInstance(best_score, float)
        self.assertIn('n_estimators', best_params)
        self.assertIn('max_depth', best_params)
        self.assertGreaterEqual(best_score, 0.0)
        self.assertLessEqual(best_score, 1.0)
    
    def test_get_feature_importance(self):
        """Test feature importance calculation"""
        # Train a model first
        model, _ = self.ml_utils.train_model(
            self.X, self.y,
            model_type='classification',
            test_size=0.2,
            random_state=42
        )
        
        importance = self.ml_utils.get_feature_importance(model, self.feature_names)
        
        # Assertions
        self.assertIsInstance(importance, dict)
        self.assertEqual(len(importance), 3)
        
        for feature in self.feature_names:
            self.assertIn(feature, importance)
            self.assertIsInstance(importance[feature], float)
            self.assertGreaterEqual(importance[feature], 0.0)
    
    def test_save_and_load_model(self):
        """Test model saving and loading"""
        # Train a model
        model, _ = self.ml_utils.train_model(
            self.X, self.y,
            model_type='classification',
            test_size=0.2,
            random_state=42
        )
        
        # Save model
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            temp_file = f.name
        
        try:
            self.ml_utils.save_model(model, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Load model
            loaded_model = self.ml_utils.load_model(temp_file)
            self.assertIsNotNone(loaded_model)
            
            # Test predictions
            original_pred = model.predict(self.X[:5])
            loaded_pred = loaded_model.predict(self.X[:5])
            np.testing.assert_array_equal(original_pred, loaded_pred)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = WebScraper()
    
    @patch('requests.get')
    def test_scrape_website_success(self, mock_get):
        """Test successful website scraping"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><h1>Test Content</h1></body></html>'
        mock_get.return_value = mock_response
        
        content = self.scraper.scrape_website('https://example.com')
        
        # Assertions
        self.assertIsNotNone(content)
        self.assertIn('Test Content', content)
        mock_get.assert_called_once_with('https://example.com', timeout=30)
    
    @patch('requests.get')
    def test_scrape_website_failure(self, mock_get):
        """Test website scraping failure"""
        # Mock failed response
        mock_get.side_effect = Exception('Connection error')
        
        content = self.scraper.scrape_website('https://example.com')
        
        # Assertions
        self.assertIsNone(content)
    
    @patch('requests.get')
    def test_extract_api_data_success(self, mock_get):
        """Test successful API data extraction"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'title': 'Test Post', 'body': 'Test content'}
        ]
        mock_get.return_value = mock_response
        
        data = self.scraper.extract_api_data('https://api.example.com/posts')
        
        # Assertions
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Post')
    
    def test_export_data(self):
        """Test data export functionality"""
        sample_data = {
            'articles': [
                {'title': 'Test Article', 'url': 'https://example.com'}
            ],
            'tables': [pd.DataFrame({'A': [1, 2], 'B': [3, 4]})]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.scraper.export_data(sample_data, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify exported content
            with open(temp_file, 'r') as f:
                exported_data = json.load(f)
            
            self.assertIn('articles', exported_data)
            self.assertEqual(len(exported_data['articles']), 1)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFileUtils(unittest.TestCase):
    """Test cases for FileUtils class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.file_utils = FileUtils()
        self.sample_data = {
            'users': [
                {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
            ]
        }
    
    def test_write_and_read_json(self):
        """Test JSON file operations"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Write JSON
            self.file_utils.write_json(self.sample_data, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Read JSON
            loaded_data = self.file_utils.read_json(temp_file)
            self.assertEqual(loaded_data, self.sample_data)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_write_and_read_csv(self):
        """Test CSV file operations"""
        df = pd.DataFrame(self.sample_data['users'])
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Write CSV
            self.file_utils.write_csv(df, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Read CSV
            loaded_data = self.file_utils.read_csv(temp_file)
            self.assertIsInstance(loaded_data, pd.DataFrame)
            self.assertEqual(len(loaded_data), 2)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_write_and_read_excel(self):
        """Test Excel file operations"""
        df = pd.DataFrame(self.sample_data['users'])
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file = f.name
        
        try:
            # Write Excel
            self.file_utils.write_excel(df, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Read Excel
            loaded_data = self.file_utils.read_excel(temp_file)
            self.assertIsInstance(loaded_data, pd.DataFrame)
            self.assertEqual(len(loaded_data), 2)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_directory_operations(self):
        """Test directory operations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory
            subdir = os.path.join(temp_dir, 'test_subdir')
            self.file_utils.create_directory(subdir)
            self.assertTrue(os.path.exists(subdir))
            
            # List directory
            contents = self.file_utils.list_directory(temp_dir)
            self.assertIn('test_subdir', contents)
            
            # Check if file exists
            test_file = os.path.join(temp_dir, 'test_file.txt')
            with open(test_file, 'w') as f:
                f.write('test content')
            
            exists = self.file_utils.file_exists(test_file)
            self.assertTrue(exists)
    
    def test_file_compression(self):
        """Test file compression and extraction"""
        # Create test files
        with tempfile.TemporaryDirectory() as temp_dir:
            test_files = []
            for i in range(3):
                test_file = os.path.join(temp_dir, f'test_file_{i}.txt')
                with open(test_file, 'w') as f:
                    f.write(f'content {i}')
                test_files.append(test_file)
            
            # Compress files
            archive_path = os.path.join(temp_dir, 'test_archive.zip')
            self.file_utils.compress_files(test_files, archive_path)
            self.assertTrue(os.path.exists(archive_path))
            
            # Extract files
            extract_dir = os.path.join(temp_dir, 'extracted')
            self.file_utils.extract_archive(archive_path, extract_dir)
            self.assertTrue(os.path.exists(extract_dir))
            
            # Check extracted files
            extracted_files = os.listdir(extract_dir)
            self.assertEqual(len(extracted_files), 3)
    
    def test_get_file_info(self):
        """Test file information retrieval"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
            f.write(b'test content')
        
        try:
            file_info = self.file_utils.get_file_info(temp_file)
            
            # Assertions
            self.assertIsInstance(file_info, dict)
            self.assertIn('size', file_info)
            self.assertIn('created', file_info)
            self.assertIn('modified', file_info)
            self.assertIn('type', file_info)
            
            self.assertEqual(file_info['size'], 12)  # 'test content' length
            self.assertIsInstance(file_info['created'], str)
            self.assertIsInstance(file_info['modified'], str)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_search_files(self):
        """Test file search functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = [
                'test1.json',
                'test2.csv',
                'test3.txt',
                'data.json'
            ]
            
            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write('test content')
            
            # Search for JSON files
            json_files = self.file_utils.search_files(temp_dir, '*.json')
            self.assertEqual(len(json_files), 2)
            self.assertTrue(all(f.endswith('.json') for f in json_files))


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components"""
    
    def test_data_processing_pipeline(self):
        """Test complete data processing pipeline"""
        processor = DataProcessor()
        file_utils = FileUtils()
        
        # Create sample data
        sample_data = pd.DataFrame({
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 75000],
            'department': ['IT', 'HR', 'IT']
        })
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save data
            processor.save_data(sample_data, temp_file)
            
            # Load data
            loaded_data = processor.load_data(temp_file)
            
            # Clean data
            cleaned_data = processor.clean_data(loaded_data)
            
            # Transform data
            transformations = {
                'salary_category': lambda x: np.where(x['salary'] > 65000, 'High', 'Medium')
            }
            transformed_data = processor.transform_data(cleaned_data, transformations)
            
            # Export data
            output_file = temp_file.replace('.csv', '_processed.xlsx')
            processor.export_data(transformed_data, output_file)
            
            # Verify pipeline
            self.assertTrue(os.path.exists(output_file))
            self.assertIn('salary_category', transformed_data.columns)
            
        finally:
            for file in [temp_file, temp_file.replace('.csv', '_processed.xlsx')]:
                if os.path.exists(file):
                    os.unlink(file)
    
    def test_ml_pipeline_with_data_processing(self):
        """Test ML pipeline with data processing"""
        processor = DataProcessor()
        ml_utils = MLUtils()
        
        # Create synthetic data
        np.random.seed(42)
        X = np.random.randn(100, 3)
        y = (X[:, 0] + X[:, 1] * 2 + np.random.randn(100) * 0.1 > 0).astype(int)
        
        # Convert to DataFrame
        df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3'])
        df['target'] = y
        
        # Clean data
        cleaned_data = processor.clean_data(df)
        
        # Prepare features and target
        X_clean = cleaned_data[['feature_1', 'feature_2', 'feature_3']].values
        y_clean = cleaned_data['target'].values
        
        # Train model
        model, metrics = ml_utils.train_model(
            X_clean, y_clean,
            model_type='classification',
            test_size=0.2,
            random_state=42
        )
        
        # Verify pipeline
        self.assertIsNotNone(model)
        self.assertIn('accuracy', metrics)
        self.assertGreaterEqual(metrics['accuracy'], 0.0)


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDataProcessor,
        TestMLUtils,
        TestWebScraper,
        TestFileUtils,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)