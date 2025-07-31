#!/usr/bin/env python3
"""
Database configuration and connection management for SiteScanner
Handles PostgreSQL connections for the shared site_analysis database
"""

import os
import psycopg2
import psycopg2.extras
from typing import Optional, Dict, Any
import yaml
from pathlib import Path

class DatabaseConfig:
    """Database configuration manager"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize database configuration
        
        Args:
            config_path: Path to environment.yml config file. If None, uses project default.
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        
    def _find_config_file(self) -> str:
        """Find the environment.yml file in the project"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent  # Go up to project root (backend/src/database -> SiteScanner)
        config_file = project_root / "environment.yml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Could not find environment.yml at {config_file}")
            
        return str(config_file)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_database_url(self, db_type: str = 'primary') -> str:
        """Get database connection URL
        
        Args:
            db_type: Type of database ('primary', 'development', 'testing')
            
        Returns:
            Database connection URL
        """
        db_config = self.config.get('database', {})
        
        if db_type == 'primary':
            return db_config.get('primary', {}).get('url', 'postgresql://dev_user@localhost:5432/site_analysis')
        elif db_type == 'development':
            return db_config.get('development', {}).get('url', 'postgresql://dev_user@localhost:5432/sitescanner_dev')
        elif db_type == 'testing':
            return db_config.get('testing', {}).get('url', 'postgresql://dev_user@localhost:5432/sitescanner_test')
        else:
            raise ValueError(f"Unknown database type: {db_type}")
    
    def get_connection_params(self, db_type: str = 'primary') -> Dict[str, Any]:
        """Get database connection parameters as dict
        
        Args:
            db_type: Type of database ('primary', 'development', 'testing')
            
        Returns:
            Connection parameters dict
        """
        url = self.get_database_url(db_type)
        
        # Parse PostgreSQL URL: postgresql://user@host:port/database
        if url.startswith('postgresql://'):
            parts = url.replace('postgresql://', '').split('/')
            auth_host = parts[0]
            database = parts[1] if len(parts) > 1 else 'site_analysis'
            
            if '@' in auth_host:
                user, host_port = auth_host.split('@')
            else:
                user = 'dev_user'
                host_port = auth_host
                
            if ':' in host_port:
                host, port = host_port.split(':')
                port = int(port)
            else:
                host = host_port
                port = 5432
                
            return {
                'host': host,
                'port': port,
                'database': database,
                'user': user,
                'password': None  # No password for local development
            }
        else:
            raise ValueError(f"Unsupported database URL format: {url}")

class DatabaseConnection:
    """Database connection manager with context manager support"""
    
    def __init__(self, db_type: str = 'primary', config_path: Optional[str] = None):
        """Initialize database connection
        
        Args:
            db_type: Type of database ('primary', 'development', 'testing')
            config_path: Path to environment.yml config file
        """
        self.db_config = DatabaseConfig(config_path)
        self.db_type = db_type
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        if self.connection is not None:
            return self.connection
            
        try:
            params = self.db_config.get_connection_params(self.db_type)
            self.connection = psycopg2.connect(**params)
            self.connection.set_client_encoding('UTF8')
            return self.connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.db_type} database: {e}")
    
    def get_cursor(self, cursor_factory=None):
        """Get database cursor
        
        Args:
            cursor_factory: psycopg2 cursor factory (e.g., RealDictCursor for dict results)
            
        Returns:
            Database cursor
        """
        if self.connection is None:
            self.connect()
            
        cursor_factory = cursor_factory or psycopg2.extras.RealDictCursor
        return self.connection.cursor(cursor_factory=cursor_factory)
    
    def execute_query(self, query: str, params: Optional[tuple] = None, fetch: str = 'all'):
        """Execute a query and return results
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            fetch: Result fetch mode ('all', 'one', 'many', 'none')
            
        Returns:
            Query results based on fetch mode
        """
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            
            if fetch == 'all':
                return cursor.fetchall()
            elif fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'many':
                return cursor.fetchmany()
            elif fetch == 'none':
                self.connection.commit()
                return cursor.rowcount
            else:
                raise ValueError(f"Invalid fetch mode: {fetch}")
                
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_many(self, query: str, params_list: list):
        """Execute query with multiple parameter sets
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        cursor = self.get_cursor()
        try:
            cursor.executemany(query, params_list)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.close()

def get_db_connection(db_type: str = 'primary') -> DatabaseConnection:
    """Convenience function to get a database connection
    
    Args:
        db_type: Type of database ('primary', 'development', 'testing')
        
    Returns:
        DatabaseConnection instance
    """
    return DatabaseConnection(db_type)

def test_connection(db_type: str = 'primary') -> bool:
    """Test database connection
    
    Args:
        db_type: Type of database to test
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        with get_db_connection(db_type) as db:
            result = db.execute_query("SELECT 1 as test", fetch='one')
            return result['test'] == 1
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Test database connections
    print("Testing database connections...")
    
    for db_type in ['primary', 'development', 'testing']:
        print(f"Testing {db_type} database...", end=' ')
        if test_connection(db_type):
            print("✅ OK")
        else:
            print("❌ FAILED")