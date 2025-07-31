#!/usr/bin/env python3
"""
Basic Scanner - Path Discovery from index.html
Collects navigation paths and identifies leaf nodes using Selenium browser crawling.
"""

import os
import sys
import time
from urllib.parse import urljoin, urlparse
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

class BasicPathScanner:
    def __init__(self, root_path, output_file=None):
        self.root_path = root_path
        self.root_url = f"file://{root_path}/index.html"
        self.base_url = f"file://{root_path}/"
        self.output_file = output_file
        
        # Data structures
        self.visited_urls = set()
        self.url_queue = deque([self.root_url])
        self.paths_found = []
        self.leaf_nodes = []
        
        # Initialize Chrome driver
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        """Setup headless Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def _is_internal_url(self, url):
        """Check if URL is within our site directory"""
        if url.startswith(self.base_url):
            return True
        if url.startswith("file://") and self.root_path in url:
            return True
        return False
    
    def _file_exists(self, url):
        """Check if the file exists on filesystem"""
        if url.startswith("file://"):
            file_path = url.replace("file://", "")
            return os.path.exists(file_path)
        return False
    
    def _log(self, message):
        """Write message to output file or print to console"""
        if self.output_file:
            with open(self.output_file, 'a') as f:
                f.write(message + '\n')
        else:
            print(message)
    
    def _extract_links(self, url):
        """Extract all links from current page"""
        try:
            # Only log the relative path from root
            relative_url = url.replace(self.base_url, "")
            self._log(f"Crawling: {relative_url}")
            self.driver.get(url)
            
            # Wait for JavaScript to finish executing
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for any lazy-loaded content
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find all links
            link_elements = self.driver.find_elements("tag name", "a")
            links = []
            
            for element in link_elements:
                href = element.get_attribute("href")
                if href:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(url, href)
                    if self._is_internal_url(absolute_url) and self._file_exists(absolute_url):
                        links.append(absolute_url)
            
            return links
            
        except Exception as e:
            relative_url = url.replace(self.base_url, "")
            self._log(f"Error crawling {relative_url}: {e}")
            return []
    
    def _is_leaf_node(self, links):
        """Determine if a page is a leaf node (no outgoing internal links)"""
        internal_links = [link for link in links if link not in self.visited_urls]
        return len(internal_links) == 0
    
    def scan_paths(self, max_leaf_nodes=50):
        """Scan for paths and identify leaf nodes"""
        self._log(f"Starting scan from: {self.root_url.replace(self.base_url, '')}")
        self._log(f"Target: {max_leaf_nodes} leaf nodes")
        self._log("-" * 60)
        
        while self.url_queue and len(self.leaf_nodes) < max_leaf_nodes:
            current_url = self.url_queue.popleft()
            
            if current_url in self.visited_urls:
                continue
                
            self.visited_urls.add(current_url)
            
            # Extract links from current page
            links = self._extract_links(current_url)
            
            # Add new links to queue
            new_links = [link for link in links if link not in self.visited_urls]
            self.url_queue.extend(new_links)
            
            # Check if this is a leaf node
            if self._is_leaf_node(links):
                self.leaf_nodes.append(current_url)
                relative_url = current_url.replace(self.base_url, "")
                self._log(f"LEAF NODE #{len(self.leaf_nodes)}: {relative_url}")
            
            # Track path
            self.paths_found.append({
                'url': current_url,
                'outgoing_links': len(links),
                'is_leaf': current_url in self.leaf_nodes
            })
            
            self._log(f"Pages crawled: {len(self.visited_urls)}, Queue: {len(self.url_queue)}, Leaves: {len(self.leaf_nodes)}")
        
        self._log("-" * 60)
        self._log("SCAN COMPLETE")
        self._log(f"Total pages crawled: {len(self.visited_urls)}")
        self._log(f"Leaf nodes found: {len(self.leaf_nodes)}")
        
        return self.leaf_nodes
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    root_path = "/Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com"
    
    # Get max_leaf_nodes from command line or default to 50
    max_leaf_nodes = 50
    if len(sys.argv) > 1:
        try:
            max_leaf_nodes = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}, using default of 50")
    
    # Create output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"scan_output_{timestamp}.txt"
    
    scanner = BasicPathScanner(root_path, output_file=output_file)
    
    try:
        leaf_nodes = scanner.scan_paths(max_leaf_nodes=max_leaf_nodes)
        
        scanner._log("\n" + "="*60)
        scanner._log("LEAF NODES SUMMARY:")
        scanner._log("="*60)
        for i, leaf in enumerate(leaf_nodes, 1):
            relative_leaf = leaf.replace(scanner.base_url, "")
            scanner._log(f"{i:2d}. {relative_leaf}")
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        scanner._log("\nScan interrupted by user")
    except Exception as e:
        print(f"Error during scan: {e}")
        scanner._log(f"Error during scan: {e}")
    finally:
        scanner.close()
        print(f"\nOutput saved to: {output_file}")

if __name__ == "__main__":
    main()