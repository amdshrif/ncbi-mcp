"""
Tool schema definitions for NCBI MCP Server.
"""

import mcp.types as types
from typing import List


def get_tool_schemas() -> List[types.Tool]:
    """Get all tool schema definitions."""
    return [
        types.Tool(
            name="esearch",
            description="Search NCBI databases for records matching a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name (e.g., pubmed, protein, nuccore, gene)"
                    },
                    "term": {
                        "type": "string",
                        "description": "Search query (e.g., 'cancer therapy', 'insulin[protein]')"
                    },
                    "retmax": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 20, max: 10000)",
                        "default": 20
                    },
                    "retstart": {
                        "type": "integer",
                        "description": "Starting index for results (default: 0)",
                        "default": 0
                    },
                    "sort": {
                        "type": "string",
                        "description": "Sort order (e.g., relevance, pub_date, author)"
                    },
                    "field": {
                        "type": "string",
                        "description": "Search field to limit search (e.g., title, author)"
                    },
                    "datetype": {
                        "type": "string",
                        "description": "Date type for date range (pdat, mdat, edat)"
                    },
                    "reldate": {
                        "type": "integer",
                        "description": "Days back from today for search"
                    },
                    "mindate": {
                        "type": "string",
                        "description": "Start date (YYYY/MM/DD format)"
                    },
                    "maxdate": {
                        "type": "string",
                        "description": "End date (YYYY/MM/DD format)"
                    },
                    "usehistory": {
                        "type": "boolean",
                        "description": "Store results on history server for large datasets",
                        "default": False
                    }
                },
                "required": ["db", "term"]
            }
        ),
        types.Tool(
            name="efetch",
            description="Retrieve full records from NCBI databases by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "id_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of record IDs to fetch"
                    },
                    "rettype": {
                        "type": "string",
                        "description": "Retrieval type (abstract, fasta, gb, docsum, etc.)",
                        "default": "docsum"
                    },
                    "retmode": {
                        "type": "string",
                        "description": "Retrieval mode (xml, text, json)",
                        "default": "xml"
                    },
                    "retstart": {
                        "type": "integer",
                        "description": "Starting index",
                        "default": 0
                    },
                    "retmax": {
                        "type": "integer",
                        "description": "Maximum records to fetch"
                    },
                    "strand": {
                        "type": "integer",
                        "description": "DNA strand (1 or 2)"
                    },
                    "seq_start": {
                        "type": "integer",
                        "description": "Sequence start position"
                    },
                    "seq_stop": {
                        "type": "integer",
                        "description": "Sequence stop position"
                    },
                    "webenv": {
                        "type": "string",
                        "description": "Web environment from history server"
                    },
                    "query_key": {
                        "type": "integer",
                        "description": "Query key from history server"
                    }
                },
                "anyOf": [
                    {"required": ["db", "id_list"]},
                    {"required": ["db", "webenv", "query_key"]}
                ]
            }
        ),
        types.Tool(
            name="esummary",
            description="Get document summaries with key metadata for records",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "id_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of record IDs"
                    },
                    "version": {
                        "type": "string",
                        "description": "ESummary version (1.0 or 2.0)",
                        "default": "1.0"
                    },
                    "retstart": {
                        "type": "integer",
                        "description": "Starting index",
                        "default": 0
                    },
                    "retmax": {
                        "type": "integer",
                        "description": "Maximum records to return"
                    },
                    "webenv": {
                        "type": "string",
                        "description": "Web environment from history server"
                    },
                    "query_key": {
                        "type": "integer",
                        "description": "Query key from history server"
                    }
                },
                "anyOf": [
                    {"required": ["db", "id_list"]},
                    {"required": ["db", "webenv", "query_key"]}
                ]
            }
        ),
        types.Tool(
            name="epost",
            description="Upload ID lists to NCBI history server for efficient batch processing",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "id_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of record IDs to post"
                    },
                    "webenv": {
                        "type": "string",
                        "description": "Existing web environment to append to"
                    }
                },
                "required": ["db", "id_list"]
            }
        ),
        types.Tool(
            name="elink",
            description="Find related records across NCBI databases",
            inputSchema={
                "type": "object",
                "properties": {
                    "dbfrom": {
                        "type": "string",
                        "description": "Source database name"
                    },
                    "db": {
                        "type": "string",
                        "description": "Target database name"
                    },
                    "id_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of source record IDs"
                    },
                    "cmd": {
                        "type": "string",
                        "description": "Link command (neighbor, neighbor_score, etc.)",
                        "default": "neighbor"
                    },
                    "linkname": {
                        "type": "string",
                        "description": "Specific link type"
                    },
                    "term": {
                        "type": "string",
                        "description": "Filter term for linked results"
                    },
                    "holding": {
                        "type": "string",
                        "description": "Holding library"
                    },
                    "webenv": {
                        "type": "string",
                        "description": "Web environment from history server"
                    },
                    "query_key": {
                        "type": "integer",
                        "description": "Query key from history server"
                    }
                },
                "anyOf": [
                    {"required": ["dbfrom", "db", "id_list"]},
                    {"required": ["dbfrom", "db", "webenv", "query_key"]}
                ]
            }
        ),
        types.Tool(
            name="einfo",
            description="Get information about NCBI databases and search fields",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name (omit to get list of all databases)"
                    },
                    "retmode": {
                        "type": "string",
                        "description": "Return mode (xml or json)",
                        "default": "xml"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="egquery",
            description="Search all NCBI databases simultaneously with a single query",
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Search term to query across all databases"
                    }
                },
                "required": ["term"]
            }
        ),
        types.Tool(
            name="espell",
            description="Get spelling suggestions for search terms",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "term": {
                        "type": "string",
                        "description": "Search term to check spelling"
                    }
                },
                "required": ["db", "term"]
            }
        ),
        types.Tool(
            name="ecitmatch",
            description="Match citations to PubMed IDs",
            inputSchema={
                "type": "object",
                "properties": {
                    "citations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of citation strings in NCBI format"
                    },
                    "db": {
                        "type": "string",
                        "description": "Database (usually pubmed)",
                        "default": "pubmed"
                    }
                },
                "required": ["citations"]
            }
        ),
        types.Tool(
            name="search_and_fetch",
            description="Combined search and fetch operation for common workflows",
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": "Database name"
                    },
                    "term": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "retmax": {
                        "type": "integer",
                        "description": "Maximum results to search and fetch",
                        "default": 10
                    },
                    "rettype": {
                        "type": "string",
                        "description": "Fetch retrieval type",
                        "default": "abstract"
                    },
                    "retmode": {
                        "type": "string",
                        "description": "Fetch retrieval mode",
                        "default": "text"
                    }
                },
                "required": ["db", "term"]
            }
        ),
        types.Tool(
            name="get_databases",
            description="Get list of all available NCBI databases",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="server_info",
            description="Get information about the NCBI-MCP server, its capabilities, author, and general overview",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]
