"""
NCBI MCP Server - Model Context Protocol server for NCBI E-utilities.

This server provides comprehensive access to all NCBI E-utilities through the Model Context Protocol,
enabling LLMs to search, fetch, and analyze biological data from NCBI databases.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from .schemas import get_tool_schemas
from .handlers import tool_handlers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
server = Server("ncbi-mcp")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List all available NCBI tools."""
    return get_tool_schemas()


@server.call_tool()
async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[types.TextContent]:
    """Handle tool calls from the MCP client."""
    
    try:
        result = tool_handlers.dispatch(name, arguments or {})
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        logger.error(f"Tool call failed: {e}")
        raise


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting NCBI MCP Server...")
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ncbi-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
