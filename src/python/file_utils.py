"""
File Utilities Module

This module provides comprehensive file handling and I/O operations utilities.
It includes functions for file operations, directory management, and data
serialization across various formats.

Classes:
    FileUtils: Main class for file operations

Examples:
    >>> from jagarnath.file_utils import FileUtils
    >>> file_utils = FileUtils()
    >>> data = file_utils.read_json("data.json")
    >>> file_utils.write_csv(data, "output.csv")
"""

import os
import json
import csv
import pickle
import yaml
import xml.etree.ElementTree as ET
import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import shutil
import zipfile
import tarfile
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class FileUtils:
    """
    Comprehensive file handling and I/O operations utilities.
    
    This class provides extensive file operation capabilities including:
    - File reading and writing in various formats
    - Directory operations and management
    - File compression and archiving
    - Data serialization and deserialization
    - File validation and integrity checking
    - Batch file operations
    
    Attributes:
        supported_formats (List[str]): List of supported file formats
        default_encoding (str): Default encoding for text files
        backup_enabled (bool): Whether to create backups before overwriting
        
    Examples:
        >>> file_utils = FileUtils()
        >>> data = file_utils.read_json("config.json")
        >>> file_utils.write_yaml(data, "config.yaml")
        >>> file_utils.compress_directory("data/", "archive.zip")
    """
    
    def __init__(self, encoding: str = "utf-8", backup_enabled: bool = True):
        """
        Initialize the FileUtils.
        
        Args:
            encoding (str): Default encoding for text files. Defaults to "utf-8".
            backup_enabled (bool): Whether to create backups. Defaults to True.
            
        Examples:
            >>> file_utils = FileUtils(encoding="latin-1", backup_enabled=False)
        """
        self.supported_formats = ['.json', '.csv', '.yaml', '.yml', '.xml', '.txt', '.pickle', '.pkl']
        self.default_encoding = encoding
        self.backup_enabled = backup_enabled
        
    def read_json(self, file_path: str, **kwargs) -> Union[Dict, List]:
        """
        Read data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            **kwargs: Additional arguments passed to json.load()
            
        Returns:
            Union[Dict, List]: Parsed JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file is not valid JSON
            
        Examples:
            >>> data = file_utils.read_json("config.json")
            >>> data = file_utils.read_json("data.json", encoding="latin-1")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                data = json.load(f, **kwargs)
                
            logger.info(f"Successfully read JSON file: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise
            
    def write_json(self, data: Union[Dict, List], file_path: str, 
                   indent: int = 2, **kwargs) -> None:
        """
        Write data to a JSON file.
        
        Args:
            data (Union[Dict, List]): Data to write
            file_path (str): Output file path
            indent (int): JSON indentation. Defaults to 2.
            **kwargs: Additional arguments passed to json.dump()
            
        Examples:
            >>> file_utils.write_json(data, "output.json")
            >>> file_utils.write_json(data, "output.json", indent=4, sort_keys=True)
        """
        try:
            file_path = Path(file_path)
            
            # Create backup if enabled
            if self.backup_enabled and file_path.exists():
                self._create_backup(file_path)
                
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=self.default_encoding) as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, **kwargs)
                
            logger.info(f"Successfully wrote JSON file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {str(e)}")
            raise
            
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Read data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            **kwargs: Additional arguments passed to pandas.read_csv()
            
        Returns:
            pd.DataFrame: Loaded data as a pandas DataFrame
            
        Examples:
            >>> df = file_utils.read_csv("data.csv")
            >>> df = file_utils.read_csv("data.csv", sep=";", encoding="latin-1")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            # Set default parameters
            default_params = {
                'encoding': self.default_encoding
            }
            default_params.update(kwargs)
            
            data = pd.read_csv(file_path, **default_params)
            logger.info(f"Successfully read CSV file: {file_path} with {len(data)} rows")
            return data
            
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            raise
            
    def write_csv(self, data: Union[pd.DataFrame, List[Dict]], file_path: str, 
                  **kwargs) -> None:
        """
        Write data to a CSV file.
        
        Args:
            data (Union[pd.DataFrame, List[Dict]]): Data to write
            file_path (str): Output file path
            **kwargs: Additional arguments passed to pandas.to_csv()
            
        Examples:
            >>> file_utils.write_csv(df, "output.csv")
            >>> file_utils.write_csv(data_list, "output.csv", index=False)
        """
        try:
            file_path = Path(file_path)
            
            # Create backup if enabled
            if self.backup_enabled and file_path.exists():
                self._create_backup(file_path)
                
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to DataFrame if needed
            if isinstance(data, list):
                data = pd.DataFrame(data)
                
            # Set default parameters
            default_params = {
                'index': False,
                'encoding': self.default_encoding
            }
            default_params.update(kwargs)
            
            data.to_csv(file_path, **default_params)
            logger.info(f"Successfully wrote CSV file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing CSV file {file_path}: {str(e)}")
            raise
            
    def read_yaml(self, file_path: str, **kwargs) -> Union[Dict, List]:
        """
        Read data from a YAML file.
        
        Args:
            file_path (str): Path to the YAML file
            **kwargs: Additional arguments passed to yaml.safe_load()
            
        Returns:
            Union[Dict, List]: Parsed YAML data
            
        Examples:
            >>> data = file_utils.read_yaml("config.yaml")
            >>> data = file_utils.read_yaml("settings.yml")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            with open(file_path, 'r', encoding=self.default_encoding) as f:
                data = yaml.safe_load(f, **kwargs)
                
            logger.info(f"Successfully read YAML file: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading YAML file {file_path}: {str(e)}")
            raise
            
    def write_yaml(self, data: Union[Dict, List], file_path: str, 
                   default_flow_style: bool = False, **kwargs) -> None:
        """
        Write data to a YAML file.
        
        Args:
            data (Union[Dict, List]): Data to write
            file_path (str): Output file path
            default_flow_style (bool): YAML flow style. Defaults to False.
            **kwargs: Additional arguments passed to yaml.dump()
            
        Examples:
            >>> file_utils.write_yaml(data, "config.yaml")
            >>> file_utils.write_yaml(data, "config.yaml", default_flow_style=True)
        """
        try:
            file_path = Path(file_path)
            
            # Create backup if enabled
            if self.backup_enabled and file_path.exists():
                self._create_backup(file_path)
                
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=self.default_encoding) as f:
                yaml.dump(data, f, default_flow_style=default_flow_style, 
                         allow_unicode=True, **kwargs)
                
            logger.info(f"Successfully wrote YAML file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing YAML file {file_path}: {str(e)}")
            raise
            
    def read_pickle(self, file_path: str, **kwargs) -> Any:
        """
        Read data from a pickle file.
        
        Args:
            file_path (str): Path to the pickle file
            **kwargs: Additional arguments passed to pickle.load()
            
        Returns:
            Any: Unpickled data
            
        Examples:
            >>> data = file_utils.read_pickle("model.pkl")
            >>> model = file_utils.read_pickle("trained_model.pickle")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            with open(file_path, 'rb') as f:
                data = pickle.load(f, **kwargs)
                
            logger.info(f"Successfully read pickle file: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error reading pickle file {file_path}: {str(e)}")
            raise
            
    def write_pickle(self, data: Any, file_path: str, **kwargs) -> None:
        """
        Write data to a pickle file.
        
        Args:
            data (Any): Data to pickle
            file_path (str): Output file path
            **kwargs: Additional arguments passed to pickle.dump()
            
        Examples:
            >>> file_utils.write_pickle(model, "model.pkl")
            >>> file_utils.write_pickle(data, "data.pickle", protocol=4)
        """
        try:
            file_path = Path(file_path)
            
            # Create backup if enabled
            if self.backup_enabled and file_path.exists():
                self._create_backup(file_path)
                
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                pickle.dump(data, f, **kwargs)
                
            logger.info(f"Successfully wrote pickle file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing pickle file {file_path}: {str(e)}")
            raise
            
    def read_xml(self, file_path: str) -> ET.Element:
        """
        Read data from an XML file.
        
        Args:
            file_path (str): Path to the XML file
            
        Returns:
            ET.Element: Parsed XML element tree
            
        Examples:
            >>> root = file_utils.read_xml("config.xml")
            >>> for child in root:
            >>>     print(child.tag, child.text)
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            logger.info(f"Successfully read XML file: {file_path}")
            return root
            
        except Exception as e:
            logger.error(f"Error reading XML file {file_path}: {str(e)}")
            raise
            
    def write_xml(self, element: ET.Element, file_path: str, 
                  encoding: str = "utf-8", **kwargs) -> None:
        """
        Write XML element to file.
        
        Args:
            element (ET.Element): XML element to write
            file_path (str): Output file path
            encoding (str): XML encoding. Defaults to "utf-8".
            **kwargs: Additional arguments passed to ET.ElementTree.write()
            
        Examples:
            >>> file_utils.write_xml(root, "output.xml")
            >>> file_utils.write_xml(element, "config.xml", encoding="latin-1")
        """
        try:
            file_path = Path(file_path)
            
            # Create backup if enabled
            if self.backup_enabled and file_path.exists():
                self._create_backup(file_path)
                
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            tree = ET.ElementTree(element)
            tree.write(file_path, encoding=encoding, xml_declaration=True, **kwargs)
            
            logger.info(f"Successfully wrote XML file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error writing XML file {file_path}: {str(e)}")
            raise
            
    def compress_directory(self, source_dir: str, output_path: str, 
                          compression_type: str = "zip") -> None:
        """
        Compress a directory into an archive.
        
        Args:
            source_dir (str): Source directory to compress
            output_path (str): Output archive path
            compression_type (str): Type of compression ("zip", "tar.gz", "tar.bz2"). Defaults to "zip".
            
        Examples:
            >>> file_utils.compress_directory("data/", "archive.zip")
            >>> file_utils.compress_directory("logs/", "backup.tar.gz", "tar.gz")
        """
        try:
            source_path = Path(source_dir)
            output_path = Path(output_path)
            
            if not source_path.exists():
                raise FileNotFoundError(f"Source directory not found: {source_path}")
                
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if compression_type == "zip":
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path)
                            zipf.write(file_path, arcname)
                            
            elif compression_type in ["tar.gz", "tar.bz2"]:
                mode = 'w:gz' if compression_type == "tar.gz" else 'w:bz2'
                with tarfile.open(output_path, mode) as tar:
                    tar.add(source_path, arcname=source_path.name)
                    
            else:
                raise ValueError(f"Unsupported compression type: {compression_type}")
                
            logger.info(f"Successfully compressed {source_dir} to {output_path}")
            
        except Exception as e:
            logger.error(f"Error compressing directory {source_dir}: {str(e)}")
            raise
            
    def extract_archive(self, archive_path: str, extract_dir: str) -> None:
        """
        Extract an archive to a directory.
        
        Args:
            archive_path (str): Path to the archive file
            extract_dir (str): Directory to extract to
            
        Examples:
            >>> file_utils.extract_archive("archive.zip", "extracted/")
            >>> file_utils.extract_archive("backup.tar.gz", "restored/")
        """
        try:
            archive_path = Path(archive_path)
            extract_path = Path(extract_dir)
            
            if not archive_path.exists():
                raise FileNotFoundError(f"Archive not found: {archive_path}")
                
            # Create extract directory
            extract_path.mkdir(parents=True, exist_ok=True)
            
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(extract_path)
                    
            elif archive_path.suffix in ['.gz', '.bz2']:
                with tarfile.open(archive_path, 'r:*') as tar:
                    tar.extractall(extract_path)
                    
            else:
                raise ValueError(f"Unsupported archive format: {archive_path.suffix}")
                
            logger.info(f"Successfully extracted {archive_path} to {extract_dir}")
            
        except Exception as e:
            logger.error(f"Error extracting archive {archive_path}: {str(e)}")
            raise
            
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Dict[str, Any]: File information
            
        Examples:
            >>> info = file_utils.get_file_info("data.csv")
            >>> print(f"Size: {info['size']} bytes")
            >>> print(f"Modified: {info['modified']}")
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            stat = file_path.stat()
            
            info = {
                'name': file_path.name,
                'path': str(file_path.absolute()),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'extension': file_path.suffix,
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir(),
                'permissions': oct(stat.st_mode)[-3:],
                'md5_hash': self._calculate_md5(file_path)
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            raise
            
    def copy_file(self, source: str, destination: str, 
                  overwrite: bool = False) -> None:
        """
        Copy a file from source to destination.
        
        Args:
            source (str): Source file path
            destination (str): Destination file path
            overwrite (bool): Whether to overwrite existing file. Defaults to False.
            
        Examples:
            >>> file_utils.copy_file("source.txt", "backup.txt")
            >>> file_utils.copy_file("data.csv", "processed/data.csv", overwrite=True)
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
                
            if dest_path.exists() and not overwrite:
                raise FileExistsError(f"Destination file exists: {dest_path}")
                
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_path, dest_path)
            logger.info(f"Successfully copied {source} to {destination}")
            
        except Exception as e:
            logger.error(f"Error copying file {source} to {destination}: {str(e)}")
            raise
            
    def move_file(self, source: str, destination: str, 
                  overwrite: bool = False) -> None:
        """
        Move a file from source to destination.
        
        Args:
            source (str): Source file path
            destination (str): Destination file path
            overwrite (bool): Whether to overwrite existing file. Defaults to False.
            
        Examples:
            >>> file_utils.move_file("temp.txt", "final.txt")
            >>> file_utils.move_file("old.csv", "archive/old.csv", overwrite=True)
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")
                
            if dest_path.exists() and not overwrite:
                raise FileExistsError(f"Destination file exists: {dest_path}")
                
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source_path), str(dest_path))
            logger.info(f"Successfully moved {source} to {destination}")
            
        except Exception as e:
            logger.error(f"Error moving file {source} to {destination}: {str(e)}")
            raise
            
    def delete_file(self, file_path: str, confirm: bool = True) -> None:
        """
        Delete a file.
        
        Args:
            file_path (str): Path to the file to delete
            confirm (bool): Whether to require confirmation. Defaults to True.
            
        Examples:
            >>> file_utils.delete_file("temp.txt")
            >>> file_utils.delete_file("old.log", confirm=False)
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            if confirm:
                response = input(f"Are you sure you want to delete {file_path}? (y/N): ")
                if response.lower() != 'y':
                    logger.info("File deletion cancelled")
                    return
                    
            file_path.unlink()
            logger.info(f"Successfully deleted file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            raise
            
    def _create_backup(self, file_path: Path) -> None:
        """Create a backup of a file before overwriting."""
        backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        
    def _calculate_md5(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()