#!/usr/bin/env python3
"""
NCBI MCP Server entry point.
"""

def main():
    """Entry point for running the MCP server."""
    from .cli import cli
    cli()

if __name__ == "__main__":
    main()
