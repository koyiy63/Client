"""
Machine Learning Utilities Module

This module provides comprehensive machine learning utilities for model training,
evaluation, and prediction. It includes functions for various ML algorithms,
hyperparameter tuning, and model evaluation metrics.

Classes:
    MLUtils: Main class for machine learning operations

Examples:
    >>> from jagarnath.ml_utils import MLUtils
    >>> ml_utils = MLUtils()
    >>> model = ml_utils.train_model(data, target_column="target")
    >>> predictions = ml_utils.predict(model, new_data)
    >>> metrics = ml_utils.evaluate_model(model, test_data, test_target)
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score,
    classification_report, confusion_matrix
)
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class MLUtils:
    """
    Comprehensive machine learning utilities and model management.
    
    This class provides extensive ML capabilities including:
    - Model training with various algorithms
    - Hyperparameter tuning and optimization
    - Model evaluation and metrics calculation
    - Model persistence and loading
    - Feature importance analysis
    - Cross-validation and model selection
    
    Attributes:
        supported_models (Dict): Dictionary of supported ML models
        default_random_state (int): Default random state for reproducibility
        model_storage_path (str): Default path for model storage
        
    Examples:
        >>> ml_utils = MLUtils()
        >>> model = ml_utils.train_model(data, target="target", algorithm="random_forest")
        >>> predictions = ml_utils.predict(model, new_data)
        >>> ml_utils.save_model(model, "my_model.pkl")
    """
    
    def __init__(self, random_state: int = 42, model_storage: str = "models/"):
        """
        Initialize the MLUtils.
        
        Args:
            random_state (int): Random state for reproducibility. Defaults to 42.
            model_storage (str): Path for model storage. Defaults to "models/".
            
        Examples:
            >>> ml_utils = MLUtils(random_state=123, model_storage="my_models/")
        """
        self.default_random_state = random_state
        self.model_storage_path = Path(model_storage)
        self.model_storage_path.mkdir(exist_ok=True)
        
        # Initialize supported models
        self.supported_models = {
            'linear_regression': LinearRegression,
            'logistic_regression': LogisticRegression,
            'random_forest_classifier': RandomForestClassifier,
            'random_forest_regressor': RandomForestRegressor,
            'svm_classifier': SVC,
            'svm_regressor': SVR
        }
        
        self._training_history = {}
        
    def train_model(self, data: pd.DataFrame, 
                   target_column: str,
                   algorithm: str = "random_forest_classifier",
                   test_size: float = 0.2,
                   random_state: Optional[int] = None,
                   **model_params) -> Tuple[Any, Dict[str, Any]]:
        """
        Train a machine learning model.
        
        Args:
            data (pd.DataFrame): Training data
            target_column (str): Name of the target column
            algorithm (str): ML algorithm to use. Defaults to "random_forest_classifier".
            test_size (float): Proportion of data for testing. Defaults to 0.2.
            random_state (Optional[int]): Random state for reproducibility. Defaults to None.
            **model_params: Additional parameters for the model
            
        Returns:
            Tuple[Any, Dict[str, Any]]: Trained model and training info
            
        Raises:
            ValueError: If algorithm is not supported or target column not found
            
        Examples:
            >>> model, info = ml_utils.train_model(data, "target", "random_forest_classifier")
            >>> model, info = ml_utils.train_model(data, "price", "linear_regression", test_size=0.3)
        """
        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in data")
            
        if algorithm not in self.supported_models:
            raise ValueError(f"Algorithm '{algorithm}' not supported. Available: {list(self.supported_models.keys())}")
            
        random_state = random_state or self.default_random_state
        
        # Prepare data
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # Handle categorical variables
        X = self._encode_categorical(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features if needed
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Initialize and train model
        model_class = self.supported_models[algorithm]
        model = model_class(random_state=random_state, **model_params)
        
        logger.info(f"Training {algorithm} model...")
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = self._calculate_metrics(y_test, y_pred, algorithm)
        
        # Store training info
        training_info = {
            'algorithm': algorithm,
            'target_column': target_column,
            'features': list(X.columns),
            'train_size': len(X_train),
            'test_size': len(X_test),
            'metrics': metrics,
            'model_params': model.get_params(),
            'feature_importance': self._get_feature_importance(model, X.columns) if hasattr(model, 'feature_importances_') else None
        }
        
        self._training_history[algorithm] = training_info
        
        logger.info(f"Model training completed. {algorithm} - {metrics}")
        return model, training_info
        
    def predict(self, model: Any, data: pd.DataFrame, 
                return_probabilities: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Make predictions using a trained model.
        
        Args:
            model: Trained ML model
            data (pd.DataFrame): Data to make predictions on
            return_probabilities (bool): Whether to return probabilities for classification. Defaults to False.
            
        Returns:
            Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]: Predictions and optionally probabilities
            
        Examples:
            >>> predictions = ml_utils.predict(model, new_data)
            >>> predictions, probabilities = ml_utils.predict(model, new_data, return_probabilities=True)
        """
        # Prepare data
        data_processed = self._encode_categorical(data)
        data_scaled = StandardScaler().fit_transform(data_processed)
        
        # Make predictions
        predictions = model.predict(data_scaled)
        
        if return_probabilities and hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(data_scaled)
            return predictions, probabilities
            
        return predictions
        
    def evaluate_model(self, model: Any, test_data: pd.DataFrame, 
                      target_column: str) -> Dict[str, float]:
        """
        Evaluate a trained model on test data.
        
        Args:
            model: Trained ML model
            test_data (pd.DataFrame): Test data
            target_column (str): Name of the target column
            
        Returns:
            Dict[str, float]: Dictionary of evaluation metrics
            
        Examples:
            >>> metrics = ml_utils.evaluate_model(model, test_data, "target")
            >>> print(f"Accuracy: {metrics['accuracy']}")
        """
        X_test = test_data.drop(columns=[target_column])
        y_test = test_data[target_column]
        
        # Make predictions
        y_pred = self.predict(model, X_test)
        
        # Calculate metrics
        metrics = self._calculate_metrics(y_test, y_pred, type(model).__name__)
        
        return metrics
        
    def cross_validate(self, data: pd.DataFrame, 
                      target_column: str,
                      algorithm: str = "random_forest_classifier",
                      cv_folds: int = 5,
                      **model_params) -> Dict[str, List[float]]:
        """
        Perform cross-validation on a model.
        
        Args:
            data (pd.DataFrame): Training data
            target_column (str): Name of the target column
            algorithm (str): ML algorithm to use. Defaults to "random_forest_classifier".
            cv_folds (int): Number of cross-validation folds. Defaults to 5.
            **model_params: Additional parameters for the model
            
        Returns:
            Dict[str, List[float]]: Cross-validation results
            
        Examples:
            >>> cv_results = ml_utils.cross_validate(data, "target", "random_forest_classifier")
            >>> print(f"Mean CV accuracy: {np.mean(cv_results['accuracy'])}")
        """
        if algorithm not in self.supported_models:
            raise ValueError(f"Algorithm '{algorithm}' not supported")
            
        # Prepare data
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X = self._encode_categorical(X)
        
        # Initialize model
        model_class = self.supported_models[algorithm]
        model = model_class(random_state=self.default_random_state, **model_params)
        
        # Perform cross-validation
        cv_scores = cross_val_score(model, X, y, cv=cv_folds, scoring='accuracy')
        
        results = {
            'accuracy': cv_scores.tolist(),
            'mean_accuracy': cv_scores.mean(),
            'std_accuracy': cv_scores.std(),
            'algorithm': algorithm,
            'cv_folds': cv_folds
        }
        
        logger.info(f"Cross-validation completed. Mean accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
        return results
        
    def hyperparameter_tuning(self, data: pd.DataFrame,
                             target_column: str,
                             algorithm: str = "random_forest_classifier",
                             param_grid: Optional[Dict] = None,
                             cv_folds: int = 5) -> Tuple[Any, Dict[str, Any]]:
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            data (pd.DataFrame): Training data
            target_column (str): Name of the target column
            algorithm (str): ML algorithm to use. Defaults to "random_forest_classifier".
            param_grid (Optional[Dict]): Parameter grid for tuning. Defaults to None.
            cv_folds (int): Number of cross-validation folds. Defaults to 5.
            
        Returns:
            Tuple[Any, Dict[str, Any]]: Best model and tuning results
            
        Examples:
            >>> best_model, results = ml_utils.hyperparameter_tuning(data, "target")
            >>> print(f"Best parameters: {results['best_params']}")
        """
        if algorithm not in self.supported_models:
            raise ValueError(f"Algorithm '{algorithm}' not supported")
            
        # Default parameter grids
        default_grids = {
            'random_forest_classifier': {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5, 10]
            },
            'svm_classifier': {
                'C': [0.1, 1, 10],
                'kernel': ['rbf', 'linear'],
                'gamma': ['scale', 'auto']
            },
            'logistic_regression': {
                'C': [0.1, 1, 10],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            }
        }
        
        param_grid = param_grid or default_grids.get(algorithm, {})
        
        # Prepare data
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X = self._encode_categorical(X)
        
        # Initialize model
        model_class = self.supported_models[algorithm]
        base_model = model_class(random_state=self.default_random_state)
        
        # Perform grid search
        grid_search = GridSearchCV(
            base_model, param_grid, cv=cv_folds, scoring='accuracy', n_jobs=-1
        )
        
        logger.info(f"Starting hyperparameter tuning for {algorithm}...")
        grid_search.fit(X, y)
        
        results = {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_,
            'algorithm': algorithm
        }
        
        logger.info(f"Hyperparameter tuning completed. Best score: {results['best_score']:.4f}")
        return grid_search.best_estimator_, results
        
    def save_model(self, model: Any, filename: str, 
                   include_metadata: bool = True) -> None:
        """
        Save a trained model to disk.
        
        Args:
            model: Trained ML model
            filename (str): Name of the file to save the model
            include_metadata (bool): Whether to save training metadata. Defaults to True.
            
        Examples:
            >>> ml_utils.save_model(model, "my_model.pkl")
            >>> ml_utils.save_model(model, "model_with_metadata.pkl", include_metadata=True)
        """
        file_path = self.model_storage_path / filename
        
        # Save model
        joblib.dump(model, file_path)
        
        # Save metadata if requested
        if include_metadata:
            metadata_path = file_path.with_suffix('.json')
            metadata = {
                'model_type': type(model).__name__,
                'model_params': model.get_params(),
                'training_info': self._training_history.get(type(model).__name__, {})
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
                
        logger.info(f"Model saved to {file_path}")
        
    def load_model(self, filename: str) -> Tuple[Any, Optional[Dict]]:
        """
        Load a trained model from disk.
        
        Args:
            filename (str): Name of the file to load the model from
            
        Returns:
            Tuple[Any, Optional[Dict]]: Loaded model and metadata
            
        Examples:
            >>> model, metadata = ml_utils.load_model("my_model.pkl")
        """
        file_path = self.model_storage_path / filename
        metadata_path = file_path.with_suffix('.json')
        
        # Load model
        model = joblib.load(file_path)
        
        # Load metadata if available
        metadata = None
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                
        logger.info(f"Model loaded from {file_path}")
        return model, metadata
        
    def get_feature_importance(self, model: Any, feature_names: List[str]) -> Dict[str, float]:
        """
        Get feature importance from a trained model.
        
        Args:
            model: Trained ML model with feature_importances_ attribute
            feature_names (List[str]): List of feature names
            
        Returns:
            Dict[str, float]: Dictionary mapping feature names to importance scores
            
        Examples:
            >>> importance = ml_utils.get_feature_importance(model, feature_names)
            >>> for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
            >>>     print(f"{feature}: {score:.4f}")
        """
        if not hasattr(model, 'feature_importances_'):
            raise ValueError("Model does not have feature_importances_ attribute")
            
        importance_dict = dict(zip(feature_names, model.feature_importances_))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        
    def _encode_categorical(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables in the data."""
        data_encoded = data.copy()
        
        for column in data_encoded.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            data_encoded[column] = le.fit_transform(data_encoded[column].astype(str))
            
        return data_encoded
        
    def _calculate_metrics(self, y_true: pd.Series, y_pred: np.ndarray, 
                          algorithm: str) -> Dict[str, float]:
        """Calculate appropriate metrics based on the algorithm type."""
        metrics = {}
        
        if 'classifier' in algorithm.lower():
            metrics.update({
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred, average='weighted'),
                'recall': recall_score(y_true, y_pred, average='weighted'),
                'f1_score': f1_score(y_true, y_pred, average='weighted')
            })
        else:  # Regressor
            metrics.update({
                'mse': mean_squared_error(y_true, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
                'mae': mean_absolute_error(y_true, y_pred),
                'r2_score': r2_score(y_true, y_pred)
            })
            
        return metrics
        
    def _get_feature_importance(self, model: Any, feature_names: List[str]) -> Optional[Dict[str, float]]:
        """Get feature importance if available."""
        if hasattr(model, 'feature_importances_'):
            return self.get_feature_importance(model, feature_names)
        return None
        
    @property
    def training_history(self) -> Dict[str, Any]:
        """Get training history for all models."""
        return self._training_history.copy()