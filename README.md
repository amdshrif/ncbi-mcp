# NCBI MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to NCBI E-utilities, enabling LLMs to search, fetch, and analyze biological data from NCBI databases.

## Features

- **Complete E-utilities Support**: All 9 NCBI E-utilities (ESearch, EFetch, EPost, ESummary, ELink, EInfo, EGQuery, ESpell, ECitMatch)
- **Command Line Interface**: Full CLI for server management and tool interaction
- **Modular Architecture**: Clean separation of concerns with 5 focused modules
- **Rate Limiting**: Automatic rate limiting (3 req/sec without API key, 10 req/sec with API key)
- **History Server**: Support for NCBI history server for efficient large dataset processing
- **Error Handling**: Robust error handling with meaningful error messages
- **Production Ready**: Built on the existing robust ncbi-client package

## Installation

```bash
cd /Users/ashrif/workspace/pubmed/ncbi-mcp
pip install -e .
```

## Quick Start

### CLI Usage

```bash
# List all available tools
ncbi-mcp list-tools

# Test connectivity
ncbi-mcp test

# Search PubMed
ncbi-mcp call-tool esearch -p db=pubmed -p term=diabetes -p retmax=5

# Start MCP server
ncbi-mcp serve
# or
ncbi-mcp-server
```

### MCP Server Usage

```bash
# Start the MCP server
python -m ncbi_mcp
```

## Configuration

Set environment variables for optimal performance:

```bash
export NCBI_API_KEY="your_api_key_here"  # Optional but recommended for higher rate limits
export NCBI_EMAIL="your_email@example.com"  # Optional but recommended for identification
```

## Available Commands

- `ncbi-mcp list-tools` - List all available MCP tools
- `ncbi-mcp describe-tool <name>` - Get detailed tool information  
- `ncbi-mcp call-tool <name>` - Execute a tool with parameters
- `ncbi-mcp test` - Test connectivity with NCBI
- `ncbi-mcp serve` - Start the MCP server
- `ncbi-mcp version` - Show version information

See [CLI_REFERENCE.md](CLI_REFERENCE.md) for complete CLI documentation.

Start the MCP server:

```bash
python -m ncbi_mcp
```

Or use the entry point:

```bash
ncbi-mcp
```

## Available Tools

### Core E-utilities

1. **esearch** - Search NCBI databases
2. **efetch** - Retrieve full records
3. **esummary** - Get document summaries
4. **epost** - Upload ID lists to history server
5. **elink** - Find related records across databases
6. **einfo** - Get database information
7. **egquery** - Global search across all databases
8. **espell** - Get spelling suggestions
9. **ecitmatch** - Match citations to PMIDs

### Helper Tools

10. **search_and_fetch** - Combined search and fetch operation
11. **get_databases** - List all available NCBI databases

## Examples

The MCP client can use these tools to:

- Search PubMed for research articles
- Fetch protein sequences from NCBI
- Find related genes across species
- Get database information and search fields
- Match citations to PubMed IDs
- And much more!

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol
- `ncbi-client` - Local NCBI client package

## License

Same as the ncbi-client package.
