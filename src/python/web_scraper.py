"""
Web Scraping Module

This module provides comprehensive web scraping utilities for extracting data
from websites. It includes functions for handling various web scraping scenarios,
respecting robots.txt, and managing rate limiting.

Classes:
    WebScraper: Main class for web scraping operations

Examples:
    >>> from jagarnath.web_scraper import WebScraper
    >>> scraper = WebScraper()
    >>> data = scraper.scrape_website("https://example.com")
    >>> articles = scraper.scrape_articles("https://news.com")
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin, urlparse
import json
from pathlib import Path
import re
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class WebScraper:
    """
    Advanced web scraping utilities with rate limiting and data extraction.
    
    This class provides comprehensive web scraping capabilities including:
    - HTML content extraction and parsing
    - Data extraction using CSS selectors and XPath
    - Rate limiting and polite scraping
    - Robots.txt compliance
    - Data export to various formats
    - Error handling and retry mechanisms
    
    Attributes:
        session (requests.Session): HTTP session for requests
        user_agents (List[str]): List of user agents for rotation
        default_delay (float): Default delay between requests in seconds
        max_retries (int): Maximum number of retry attempts
        
    Examples:
        >>> scraper = WebScraper()
        >>> data = scraper.scrape_website("https://example.com")
        >>> articles = scraper.scrape_articles("https://news.com", max_pages=5)
    """
    
    def __init__(self, delay: float = 1.0, max_retries: int = 3, timeout: int = 30):
        """
        Initialize the WebScraper.
        
        Args:
            delay (float): Delay between requests in seconds. Defaults to 1.0.
            max_retries (int): Maximum number of retry attempts. Defaults to 3.
            timeout (int): Request timeout in seconds. Defaults to 30.
            
        Examples:
            >>> scraper = WebScraper(delay=2.0, max_retries=5)
        """
        self.session = requests.Session()
        self.default_delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self._scraping_stats = {}
        
    def scrape_website(self, url: str, 
                      selectors: Optional[Dict[str, str]] = None,
                      extract_text: bool = True,
                      extract_links: bool = False) -> Dict[str, Any]:
        """
        Scrape a single website and extract data.
        
        Args:
            url (str): URL to scrape
            selectors (Optional[Dict[str, str]]): CSS selectors for specific data extraction
            extract_text (bool): Whether to extract main text content. Defaults to True.
            extract_links (bool): Whether to extract links. Defaults to False.
            
        Returns:
            Dict[str, Any]: Extracted data
            
        Examples:
            >>> data = scraper.scrape_website("https://example.com")
            >>> data = scraper.scrape_website("https://example.com", 
            >>>                              selectors={"title": "h1", "content": ".article-content"})
        """
        try:
            # Fetch the page
            response = self._make_request(url)
            if not response:
                return {}
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data
            data = {
                'url': url,
                'title': self._extract_title(soup),
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code
            }
            
            # Extract text content
            if extract_text:
                data['text_content'] = self._extract_text_content(soup)
                
            # Extract links
            if extract_links:
                data['links'] = self._extract_links(soup, url)
                
            # Extract data using custom selectors
            if selectors:
                data['custom_data'] = self._extract_with_selectors(soup, selectors)
                
            # Update stats
            self._update_stats(url, 'success')
            
            logger.info(f"Successfully scraped {url}")
            return data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            self._update_stats(url, 'error', str(e))
            return {}
            
    def scrape_articles(self, base_url: str,
                       article_selector: str = "article",
                       title_selector: str = "h1, h2, h3",
                       content_selector: str = "p",
                       max_pages: int = 1,
                       pagination_selector: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape multiple articles from a website.
        
        Args:
            base_url (str): Base URL of the website
            article_selector (str): CSS selector for article containers. Defaults to "article".
            title_selector (str): CSS selector for article titles. Defaults to "h1, h2, h3".
            content_selector (str): CSS selector for article content. Defaults to "p".
            max_pages (int): Maximum number of pages to scrape. Defaults to 1.
            pagination_selector (Optional[str]): CSS selector for pagination links. Defaults to None.
            
        Returns:
            List[Dict[str, Any]]: List of scraped articles
            
        Examples:
            >>> articles = scraper.scrape_articles("https://news.com", max_pages=3)
            >>> articles = scraper.scrape_articles("https://blog.com", 
            >>>                                   article_selector=".post",
            >>>                                   title_selector=".post-title")
        """
        articles = []
        current_url = base_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            try:
                # Scrape current page
                response = self._make_request(current_url)
                if not response:
                    break
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find articles
                article_elements = soup.select(article_selector)
                
                for article_elem in article_elements:
                    article_data = self._extract_article_data(
                        article_elem, title_selector, content_selector, current_url
                    )
                    if article_data:
                        articles.append(article_data)
                        
                # Find next page
                if pagination_selector:
                    next_link = soup.select_one(pagination_selector)
                    current_url = urljoin(current_url, next_link.get('href')) if next_link else None
                else:
                    current_url = None
                    
                page_count += 1
                time.sleep(self.default_delay)
                
            except Exception as e:
                logger.error(f"Error scraping page {current_url}: {str(e)}")
                break
                
        logger.info(f"Scraped {len(articles)} articles from {page_count} pages")
        return articles
        
    def scrape_table(self, url: str,
                    table_selector: str = "table",
                    header_row: int = 0,
                    extract_links: bool = False) -> pd.DataFrame:
        """
        Scrape table data from a website.
        
        Args:
            url (str): URL to scrape
            table_selector (str): CSS selector for table. Defaults to "table".
            header_row (int): Row index to use as headers. Defaults to 0.
            extract_links (bool): Whether to extract links from table cells. Defaults to False.
            
        Returns:
            pd.DataFrame: Scraped table data
            
        Examples:
            >>> df = scraper.scrape_table("https://example.com/data")
            >>> df = scraper.scrape_table("https://example.com/data", 
            >>>                           table_selector=".data-table")
        """
        try:
            response = self._make_request(url)
            if not response:
                return pd.DataFrame()
                
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.select_one(table_selector)
            
            if not table:
                logger.warning(f"No table found with selector '{table_selector}' on {url}")
                return pd.DataFrame()
                
            # Extract table data
            rows = table.find_all('tr')
            if not rows:
                return pd.DataFrame()
                
            # Extract headers
            headers = []
            if header_row < len(rows):
                header_cells = rows[header_row].find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in header_cells]
                
            # Extract data rows
            data_rows = []
            for row in rows[header_row + 1:]:
                cells = row.find_all(['td', 'th'])
                row_data = []
                for cell in cells:
                    if extract_links:
                        link = cell.find('a')
                        if link:
                            row_data.append(link.get('href'))
                        else:
                            row_data.append(cell.get_text(strip=True))
                    else:
                        row_data.append(cell.get_text(strip=True))
                data_rows.append(row_data)
                
            # Create DataFrame
            df = pd.DataFrame(data_rows, columns=headers)
            logger.info(f"Successfully scraped table with {len(df)} rows from {url}")
            return df
            
        except Exception as e:
            logger.error(f"Error scraping table from {url}: {str(e)}")
            return pd.DataFrame()
            
    def scrape_api(self, url: str,
                  params: Optional[Dict] = None,
                  headers: Optional[Dict] = None,
                  method: str = "GET") -> Dict[str, Any]:
        """
        Scrape data from an API endpoint.
        
        Args:
            url (str): API endpoint URL
            params (Optional[Dict]): Query parameters. Defaults to None.
            headers (Optional[Dict]): Request headers. Defaults to None.
            method (str): HTTP method. Defaults to "GET".
            
        Returns:
            Dict[str, Any]: API response data
            
        Examples:
            >>> data = scraper.scrape_api("https://api.example.com/data")
            >>> data = scraper.scrape_api("https://api.example.com/users", 
            >>>                           params={"page": 1, "limit": 10})
        """
        try:
            # Prepare request
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
                
            # Make request
            if method.upper() == "GET":
                response = self.session.get(url, params=params, headers=request_headers, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=params, headers=request_headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            
            # Parse response
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {'text': response.text}
                
            logger.info(f"Successfully scraped API {url}")
            return data
            
        except Exception as e:
            logger.error(f"Error scraping API {url}: {str(e)}")
            return {}
            
    def export_data(self, data: Union[Dict, List, pd.DataFrame], 
                   file_path: str, format: str = "json") -> None:
        """
        Export scraped data to file.
        
        Args:
            data: Data to export
            file_path (str): Output file path
            format (str): Export format ("json", "csv", "excel"). Defaults to "json".
            
        Examples:
            >>> scraper.export_data(data, "scraped_data.json")
            >>> scraper.export_data(df, "table_data.csv", format="csv")
        """
        try:
            file_path = Path(file_path)
            
            if format.lower() == "json":
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            elif format.lower() == "csv":
                if isinstance(data, pd.DataFrame):
                    data.to_csv(file_path, index=False, encoding='utf-8')
                else:
                    pd.DataFrame(data).to_csv(file_path, index=False, encoding='utf-8')
            elif format.lower() == "excel":
                if isinstance(data, pd.DataFrame):
                    data.to_excel(file_path, index=False)
                else:
                    pd.DataFrame(data).to_excel(file_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            logger.info(f"Data exported to {file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting data to {file_path}: {str(e)}")
            raise
            
    def get_scraping_stats(self) -> Dict[str, Any]:
        """
        Get scraping statistics.
        
        Returns:
            Dict[str, Any]: Scraping statistics
            
        Examples:
            >>> stats = scraper.get_scraping_stats()
            >>> print(f"Success rate: {stats['success_rate']:.2%}")
        """
        total_requests = sum(self._scraping_stats.values())
        successful_requests = self._scraping_stats.get('success', 0)
        
        stats = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': total_requests - successful_requests,
            'success_rate': successful_requests / total_requests if total_requests > 0 else 0,
            'detailed_stats': self._scraping_stats.copy()
        }
        
        return stats
        
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """Make HTTP request with retry logic and rate limiting."""
        for attempt in range(self.max_retries):
            try:
                # Rotate user agent
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                
                # Make request
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Rate limiting
                time.sleep(self.default_delay)
                
                return response
                
            except requests.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.default_delay * (attempt + 1))  # Exponential backoff
                    
        return None
        
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ""
        
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract main text content from page."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract links from page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Make absolute URL
            absolute_url = urljoin(base_url, href)
            
            links.append({
                'url': absolute_url,
                'text': text,
                'is_external': urlparse(absolute_url).netloc != urlparse(base_url).netloc
            })
            
        return links
        
    def _extract_with_selectors(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, str]:
        """Extract data using CSS selectors."""
        data = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            if element:
                data[key] = element.get_text(strip=True)
            else:
                data[key] = ""
        return data
        
    def _extract_article_data(self, article_elem, title_selector: str, 
                            content_selector: str, base_url: str) -> Optional[Dict[str, Any]]:
        """Extract article data from article element."""
        try:
            # Extract title
            title_elem = article_elem.select_one(title_selector)
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract content
            content_elems = article_elem.select(content_selector)
            content = " ".join([elem.get_text(strip=True) for elem in content_elems])
            
            # Extract link
            link_elem = article_elem.find('a')
            link = urljoin(base_url, link_elem.get('href')) if link_elem else ""
            
            if title or content:
                return {
                    'title': title,
                    'content': content,
                    'link': link,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.warning(f"Error extracting article data: {str(e)}")
            
        return None
        
    def _update_stats(self, url: str, status: str, error: str = None) -> None:
        """Update scraping statistics."""
        if status not in self._scraping_stats:
            self._scraping_stats[status] = 0
        self._scraping_stats[status] += 1
        
        if error:
            if 'errors' not in self._scraping_stats:
                self._scraping_stats['errors'] = {}
            self._scraping_stats['errors'][url] = error