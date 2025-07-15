"""
Data Processing Module

This module provides comprehensive data processing utilities for cleaning,
transforming, and analyzing data. It includes functions for handling various
data formats including CSV, JSON, Excel, and database connections.

Classes:
    DataProcessor: Main class for data processing operations

Examples:
    >>> from jagarnath.data_processor import DataProcessor
    >>> processor = DataProcessor()
    >>> data = processor.load_csv("data.csv")
    >>> cleaned_data = processor.clean_data(data)
    >>> transformed_data = processor.transform_data(cleaned_data)
"""

import pandas as pd
import numpy as np
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Advanced data processing and transformation utilities.
    
    This class provides comprehensive data processing capabilities including:
    - Data loading from various sources (CSV, JSON, Excel, SQL)
    - Data cleaning and validation
    - Data transformation and feature engineering
    - Data export to multiple formats
    - Statistical analysis and reporting
    
    Attributes:
        supported_formats (List[str]): List of supported file formats
        default_encoding (str): Default encoding for file operations
        max_memory_usage (int): Maximum memory usage in MB
        
    Examples:
        >>> processor = DataProcessor()
        >>> data = processor.load_csv("data.csv")
        >>> cleaned = processor.clean_data(data)
        >>> processor.export_to_json(cleaned, "output.json")
    """
    
    def __init__(self, encoding: str = "utf-8", max_memory: int = 1024):
        """
        Initialize the DataProcessor.
        
        Args:
            encoding (str): Default encoding for file operations. Defaults to "utf-8".
            max_memory (int): Maximum memory usage in MB. Defaults to 1024.
            
        Examples:
            >>> processor = DataProcessor(encoding="latin-1", max_memory=2048)
        """
        self.supported_formats = ['.csv', '.json', '.xlsx', '.xls', '.parquet', '.feather']
        self.default_encoding = encoding
        self.max_memory_usage = max_memory
        self._processing_stats = {}
        
    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            **kwargs: Additional arguments passed to pandas.read_csv()
            
        Returns:
            pd.DataFrame: Loaded data as a pandas DataFrame
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid CSV
            
        Examples:
            >>> data = processor.load_csv("data.csv", sep=",", header=0)
            >>> data = processor.load_csv("data.csv", encoding="latin-1")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            # Set default parameters
            default_params = {
                'encoding': self.default_encoding,
                'low_memory': True
            }
            default_params.update(kwargs)
            
            data = pd.read_csv(file_path, **default_params)
            logger.info(f"Successfully loaded CSV file: {file_path} with {len(data)} rows")
            return data
            
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {str(e)}")
            raise
            
    def load_json(self, file_path: str, **kwargs) -> Union[pd.DataFrame, Dict, List]:
        """
        Load data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            **kwargs: Additional arguments passed to pandas.read_json() or json.load()
            
        Returns:
            Union[pd.DataFrame, Dict, List]: Loaded data
            
        Examples:
            >>> data = processor.load_json("data.json")
            >>> data = processor.load_json("data.json", orient="records")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            # Try to load as DataFrame first, fallback to raw JSON
            try:
                data = pd.read_json(file_path, **kwargs)
                logger.info(f"Successfully loaded JSON as DataFrame: {file_path}")
                return data
            except:
                with open(file_path, 'r', encoding=self.default_encoding) as f:
                    data = json.load(f, **kwargs)
                logger.info(f"Successfully loaded JSON as raw data: {file_path}")
                return data
                
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise
            
    def clean_data(self, data: pd.DataFrame, 
                   remove_duplicates: bool = True,
                   handle_missing: str = "drop",
                   remove_outliers: bool = False,
                   outlier_threshold: float = 3.0) -> pd.DataFrame:
        """
        Clean and preprocess the data.
        
        Args:
            data (pd.DataFrame): Input data to clean
            remove_duplicates (bool): Whether to remove duplicate rows. Defaults to True.
            handle_missing (str): Strategy for handling missing values. 
                                Options: "drop", "fill_mean", "fill_median", "fill_mode". Defaults to "drop".
            remove_outliers (bool): Whether to remove outliers using IQR method. Defaults to False.
            outlier_threshold (float): Threshold for outlier detection. Defaults to 3.0.
            
        Returns:
            pd.DataFrame: Cleaned data
            
        Examples:
            >>> cleaned = processor.clean_data(data, handle_missing="fill_mean")
            >>> cleaned = processor.clean_data(data, remove_outliers=True, outlier_threshold=2.5)
        """
        if data.empty:
            logger.warning("Input data is empty")
            return data
            
        original_shape = data.shape
        cleaned_data = data.copy()
        
        # Remove duplicates
        if remove_duplicates:
            cleaned_data = cleaned_data.drop_duplicates()
            logger.info(f"Removed {original_shape[0] - len(cleaned_data)} duplicate rows")
            
        # Handle missing values
        if handle_missing != "drop":
            for column in cleaned_data.select_dtypes(include=[np.number]).columns:
                if cleaned_data[column].isnull().any():
                    if handle_missing == "fill_mean":
                        cleaned_data[column].fillna(cleaned_data[column].mean(), inplace=True)
                    elif handle_missing == "fill_median":
                        cleaned_data[column].fillna(cleaned_data[column].median(), inplace=True)
                    elif handle_missing == "fill_mode":
                        cleaned_data[column].fillna(cleaned_data[column].mode()[0], inplace=True)
        else:
            cleaned_data = cleaned_data.dropna()
            
        # Remove outliers
        if remove_outliers:
            cleaned_data = self._remove_outliers(cleaned_data, outlier_threshold)
            
        # Update processing stats
        self._processing_stats['cleaning'] = {
            'original_shape': original_shape,
            'final_shape': cleaned_data.shape,
            'rows_removed': original_shape[0] - cleaned_data.shape[0],
            'columns_removed': original_shape[1] - cleaned_data.shape[1]
        }
        
        logger.info(f"Data cleaning completed. Shape: {original_shape} -> {cleaned_data.shape}")
        return cleaned_data
        
    def transform_data(self, data: pd.DataFrame,
                      normalize: bool = False,
                      scale_features: List[str] = None,
                      encode_categorical: bool = False,
                      create_features: bool = False) -> pd.DataFrame:
        """
        Transform and engineer features in the data.
        
        Args:
            data (pd.DataFrame): Input data to transform
            normalize (bool): Whether to normalize numerical features. Defaults to False.
            scale_features (List[str]): List of features to scale. If None, scales all numerical. Defaults to None.
            encode_categorical (bool): Whether to encode categorical variables. Defaults to False.
            create_features (bool): Whether to create new features. Defaults to False.
            
        Returns:
            pd.DataFrame: Transformed data
            
        Examples:
            >>> transformed = processor.transform_data(data, normalize=True)
            >>> transformed = processor.transform_data(data, encode_categorical=True, create_features=True)
        """
        if data.empty:
            return data
            
        transformed_data = data.copy()
        
        # Normalize numerical features
        if normalize:
            numerical_cols = transformed_data.select_dtypes(include=[np.number]).columns
            if scale_features:
                numerical_cols = [col for col in numerical_cols if col in scale_features]
                
            for col in numerical_cols:
                if transformed_data[col].std() > 0:
                    transformed_data[col] = (transformed_data[col] - transformed_data[col].mean()) / transformed_data[col].std()
                    
        # Encode categorical variables
        if encode_categorical:
            categorical_cols = transformed_data.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                transformed_data[col] = pd.Categorical(transformed_data[col]).codes
                
        # Create new features
        if create_features:
            transformed_data = self._create_features(transformed_data)
            
        logger.info(f"Data transformation completed. Shape: {transformed_data.shape}")
        return transformed_data
        
    def export_to_csv(self, data: pd.DataFrame, file_path: str, **kwargs) -> None:
        """
        Export data to CSV format.
        
        Args:
            data (pd.DataFrame): Data to export
            file_path (str): Output file path
            **kwargs: Additional arguments passed to pandas.to_csv()
            
        Examples:
            >>> processor.export_to_csv(data, "output.csv", index=False)
        """
        try:
            default_params = {
                'index': False,
                'encoding': self.default_encoding
            }
            default_params.update(kwargs)
            
            data.to_csv(file_path, **default_params)
            logger.info(f"Data exported to CSV: {file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV {file_path}: {str(e)}")
            raise
            
    def export_to_json(self, data: pd.DataFrame, file_path: str, **kwargs) -> None:
        """
        Export data to JSON format.
        
        Args:
            data (pd.DataFrame): Data to export
            file_path (str): Output file path
            **kwargs: Additional arguments passed to pandas.to_json()
            
        Examples:
            >>> processor.export_to_json(data, "output.json", orient="records")
        """
        try:
            default_params = {
                'orient': 'records',
                'indent': 2
            }
            default_params.update(kwargs)
            
            data.to_json(file_path, **default_params)
            logger.info(f"Data exported to JSON: {file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting to JSON {file_path}: {str(e)}")
            raise
            
    def get_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive statistics for the data.
        
        Args:
            data (pd.DataFrame): Data to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing various statistics
            
        Examples:
            >>> stats = processor.get_statistics(data)
            >>> print(stats['summary'])
        """
        if data.empty:
            return {}
            
        stats = {
            'shape': data.shape,
            'memory_usage': data.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
            'missing_values': data.isnull().sum().to_dict(),
            'data_types': data.dtypes.to_dict(),
            'summary': data.describe().to_dict(),
            'correlation_matrix': data.corr().to_dict() if len(data.select_dtypes(include=[np.number]).columns) > 1 else {}
        }
        
        return stats
        
    def _remove_outliers(self, data: pd.DataFrame, threshold: float) -> pd.DataFrame:
        """Remove outliers using IQR method."""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        mask = pd.Series([True] * len(data))
        
        for col in numerical_cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            mask &= (data[col] >= lower_bound) & (data[col] <= upper_bound)
            
        return data[mask]
        
    def _create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create new features from existing data."""
        # Add date features if datetime columns exist
        datetime_cols = data.select_dtypes(include=['datetime64']).columns
        for col in datetime_cols:
            data[f'{col}_year'] = data[col].dt.year
            data[f'{col}_month'] = data[col].dt.month
            data[f'{col}_day'] = data[col].dt.day
            data[f'{col}_dayofweek'] = data[col].dt.dayofweek
            
        # Add interaction features for numerical columns
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) >= 2:
            for i, col1 in enumerate(numerical_cols):
                for col2 in numerical_cols[i+1:]:
                    data[f'{col1}_{col2}_product'] = data[col1] * data[col2]
                    
        return data
        
    @property
    def processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self._processing_stats.copy()