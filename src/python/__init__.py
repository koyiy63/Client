"""
Jagarnath Python API Package

A comprehensive library providing data processing, machine learning utilities,
and web scraping tools.

Version: 1.0.0
Author: Jagarnath Team
"""

from .data_processor import DataProcessor
from .ml_utils import MLUtils
from .web_scraper import WebScraper
from .file_utils import FileUtils

__version__ = "1.0.0"
__author__ = "Jagarnath Team"
__all__ = [
    "DataProcessor",
    "MLUtils", 
    "WebScraper",
    "FileUtils"
]