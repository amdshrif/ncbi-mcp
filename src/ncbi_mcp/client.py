"""
NCBI Client wrapper and initialization.
"""

import os
import sys
import logging
from typing import Optional

try:
    from ncbi_client import NCBIClient
    from ncbi_client.core.exceptions import NCBIError, RateLimitError, NetworkError, AuthenticationError
except ImportError as e:
    print(f"Failed to import ncbi_client: {e}")
    print("Make sure the ncbi-client package is installed and accessible.")
    sys.exit(1)

logger = logging.getLogger(__name__)


class NCBIClientManager:
    """Manages NCBI client instance and configuration."""
    
    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """Initialize NCBI client manager."""
        self.api_key = api_key or os.environ.get('NCBI_API_KEY')
        self.email = email or os.environ.get('NCBI_EMAIL', 'ncbi-mcp@example.com')
        self.tool = "ncbi-mcp-server"
        
        self._client = None
        
    @property
    def client(self) -> NCBIClient:
        """Get or create NCBI client instance."""
        if self._client is None:
            self._client = NCBIClient(
                api_key=self.api_key,
                email=self.email,
                tool=self.tool
            )
            logger.info(f"Initialized NCBI client: {self._client}")
        return self._client
    
    def reinitialize(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """Reinitialize client with new credentials."""
        if api_key:
            self.api_key = api_key
        if email:
            self.email = email
        self._client = None  # Force recreation on next access


# Global client manager instance
client_manager = NCBIClientManager()


def get_ncbi_client() -> NCBIClient:
    """Get the global NCBI client instance."""
    return client_manager.client
