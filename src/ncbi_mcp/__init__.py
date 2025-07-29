"""
NCBI MCP Server - Model Context Protocol server for NCBI E-utilities.
"""

__version__ = "0.1.0"

def main() -> None:
    """Entry point for the NCBI MCP server."""
    import asyncio
    from .server import main as server_main
    asyncio.run(server_main())

def cli_main() -> None:
    """Entry point for the CLI interface."""
    from .cli import main as cli_main_func
    cli_main_func()
