"""
Error handling utilities for NCBI MCP Server.
"""

import logging
from functools import wraps
from typing import Callable, Any

import mcp.types as types

# Import exceptions from client module to avoid duplication
from .client import NCBIError, RateLimitError, NetworkError, AuthenticationError

logger = logging.getLogger(__name__)


def handle_ncbi_errors(func: Callable) -> Callable:
    """Decorator to handle NCBI client errors consistently."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.warning(f"NCBI rate limit exceeded: {e}")
            raise RuntimeError(f"NCBI rate limit exceeded: {str(e)}")
        except AuthenticationError as e:
            logger.error(f"NCBI authentication failed: {e}")
            raise RuntimeError(f"NCBI authentication failed: {str(e)}")
        except NetworkError as e:
            logger.error(f"NCBI network error: {e}")
            raise RuntimeError(f"NCBI network error: {str(e)}")
        except NCBIError as e:
            logger.error(f"NCBI error: {e}")
            raise RuntimeError(f"NCBI error: {str(e)}")
        except Exception as e:
            logger.exception("Unexpected error in NCBI operation")
            raise RuntimeError(f"Unexpected error: {str(e)}")
    return wrapper
    return wrapper


class ErrorHandler:
    """Context manager for handling NCBI errors."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        
        logger.error(f"Error in {self.operation_name}: {exc_val}")
        
        if issubclass(exc_type, RateLimitError):
            raise RuntimeError(f"NCBI rate limit exceeded in {self.operation_name}: {str(exc_val)}")
        elif issubclass(exc_type, AuthenticationError):
            raise RuntimeError(f"NCBI authentication failed in {self.operation_name}: {str(exc_val)}")
        elif issubclass(exc_type, NetworkError):
            raise RuntimeError(f"NCBI network error in {self.operation_name}: {str(exc_val)}")
        elif issubclass(exc_type, NCBIError):
            raise RuntimeError(f"NCBI error in {self.operation_name}: {str(exc_val)}")
        else:
            raise RuntimeError(f"Unexpected error in {self.operation_name}: {str(exc_val)}")
        
        return True  # Suppress the original exception
        
        return True  # Suppress the original exception
