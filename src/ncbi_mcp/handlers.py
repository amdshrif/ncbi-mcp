"""
Tool handlers for NCBI E-utilities.
"""

import json
import logging
from typing import Dict, Any

from .client import get_ncbi_client
from .errors import handle_ncbi_errors

logger = logging.getLogger(__name__)


class NCBIToolHandlers:
    """Collection of NCBI tool handlers."""
    
    def __init__(self):
        self.client = get_ncbi_client()
    
    @handle_ncbi_errors
    def handle_esearch(self, args: Dict[str, Any]) -> str:
        """Handle ESearch tool."""
        db = args["db"]
        term = args["term"]
        
        # Extract optional parameters
        kwargs = {k: v for k, v in args.items() if k not in ["db", "term"] and v is not None}
        
        logger.info(f"ESearch: db={db}, term={term}, kwargs={kwargs}")
        
        if args.get("usehistory", False):
            result = self.client.esearch.search_with_history(db=db, term=term, **kwargs)
        else:
            result = self.client.esearch.search(db=db, term=term, **kwargs)
        
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_efetch(self, args: Dict[str, Any]) -> str:
        """Handle EFetch tool."""
        db = args["db"]
        
        logger.info(f"EFetch: db={db}, args={list(args.keys())}")
        
        # Check if using history server or ID list
        if "webenv" in args and "query_key" in args:
            webenv = args["webenv"]
            query_key = args["query_key"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["db", "webenv", "query_key"] and v is not None}
            result = self.client.efetch.fetch_from_history(
                db=db, webenv=webenv, query_key=query_key, **kwargs
            )
        else:
            id_list = args["id_list"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["db", "id_list"] and v is not None}
            result = self.client.efetch.fetch(db=db, id_list=id_list, **kwargs)
        
        return result
    
    @handle_ncbi_errors
    def handle_esummary(self, args: Dict[str, Any]) -> str:
        """Handle ESummary tool."""
        db = args["db"]
        
        logger.info(f"ESummary: db={db}, args={list(args.keys())}")
        
        # Check if using history server or ID list
        if "webenv" in args and "query_key" in args:
            webenv = args["webenv"]
            query_key = args["query_key"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["db", "webenv", "query_key"] and v is not None}
            result = self.client.esummary.summary_from_history(
                db=db, webenv=webenv, query_key=query_key, **kwargs
            )
        else:
            id_list = args["id_list"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["db", "id_list"] and v is not None}
            result = self.client.esummary.summary(db=db, id_list=id_list, **kwargs)
        
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_epost(self, args: Dict[str, Any]) -> str:
        """Handle EPost tool."""
        db = args["db"]
        id_list = args["id_list"]
        webenv = args.get("webenv")
        
        logger.info(f"EPost: db={db}, id_count={len(id_list)}")
        
        result = self.client.epost.post(db=db, id_list=id_list, webenv=webenv)
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_elink(self, args: Dict[str, Any]) -> str:
        """Handle ELink tool."""
        dbfrom = args["dbfrom"]
        db = args["db"]
        
        logger.info(f"ELink: dbfrom={dbfrom}, db={db}")
        
        # Check if using history server or ID list
        if "webenv" in args and "query_key" in args:
            webenv = args["webenv"]
            query_key = args["query_key"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["dbfrom", "db", "webenv", "query_key"] and v is not None}
            result = self.client.elink.link_from_history(
                dbfrom=dbfrom, db=db, webenv=webenv, query_key=query_key, **kwargs
            )
        else:
            id_list = args["id_list"]
            kwargs = {k: v for k, v in args.items() 
                     if k not in ["dbfrom", "db", "id_list"] and v is not None}
            result = self.client.elink.link(dbfrom=dbfrom, db=db, id_list=id_list, **kwargs)
        
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_einfo(self, args: Dict[str, Any]) -> str:
        """Handle EInfo tool."""
        db = args.get("db")
        
        logger.info(f"EInfo: db={db}")
        
        if db:
            # Get specific database info
            result = self.client.einfo.get_database_info(db)
        else:
            # Get list of all databases
            result = {"databases": self.client.einfo.get_databases()}
        
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_egquery(self, args: Dict[str, Any]) -> str:
        """Handle EGQuery tool."""
        term = args["term"]
        
        logger.info(f"EGQuery: term={term}")
        
        result = self.client.egquery.global_search(term)
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_espell(self, args: Dict[str, Any]) -> str:
        """Handle ESpell tool."""
        db = args["db"]
        term = args["term"]
        
        logger.info(f"ESpell: db={db}, term={term}")
        
        result = self.client.espell.spell_check(db=db, term=term)
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_ecitmatch(self, args: Dict[str, Any]) -> str:
        """Handle ECitMatch tool."""
        citations = args["citations"]
        db = args.get("db", "pubmed")
        
        logger.info(f"ECitMatch: db={db}, citation_count={len(citations)}")
        
        result = self.client.ecitmatch.citation_match(db=db, citations=citations)
        return json.dumps(result, indent=2)
    
    @handle_ncbi_errors
    def handle_search_and_fetch(self, args: Dict[str, Any]) -> str:
        """Handle combined search and fetch operation."""
        db = args["db"]
        term = args["term"]
        retmax = args.get("retmax", 10)
        rettype = args.get("rettype", "abstract")
        retmode = args.get("retmode", "text")
        
        logger.info(f"SearchAndFetch: db={db}, term={term}, retmax={retmax}")
        
        # First search
        search_result = self.client.esearch.search(db=db, term=term, retmax=retmax)
        
        if not search_result.get("id_list"):
            return f"No results found for query: {term}"
        
        # Then fetch
        fetch_result = self.client.efetch.fetch(
            db=db,
            id_list=search_result["id_list"],
            rettype=rettype,
            retmode=retmode
        )
        
        # Combine results
        combined_result = {
            "search_info": {
                "query": term,
                "total_found": search_result.get("count", 0),
                "returned": len(search_result["id_list"])
            },
            "records": fetch_result
        }
        
        if retmode.lower() == "json":
            return json.dumps(combined_result, indent=2)
        else:
            # For text/xml modes, return formatted text
            result_text = f"Search Results for: {term}\n"
            result_text += f"Total found: {search_result.get('count', 0)}\n"
            result_text += f"Returned: {len(search_result['id_list'])}\n"
            result_text += "-" * 50 + "\n"
            result_text += fetch_result
            return result_text
    
    @handle_ncbi_errors
    def handle_get_databases(self, args: Dict[str, Any]) -> str:
        """Handle get databases tool."""
        logger.info("GetDatabases: retrieving available databases")
        
        databases = self.client.get_databases()
        result = {
            "available_databases": databases,
            "count": len(databases)
        }
        return json.dumps(result, indent=2)
    
    def handle_server_info(self, args: Dict[str, Any]) -> str:
        """Handle server info tool - provides information about NCBI-MCP server."""
        logger.info("ServerInfo: retrieving server information")
        
        server_info = {
            "server_name": "NCBI-MCP Server",
            "version": "0.1.0",
            "description": "A Model Context Protocol (MCP) server that provides comprehensive access to NCBI E-utilities, enabling LLMs to search, fetch, and analyze biological data from NCBI databases.",
            "author": {
                "name": "Ahmad Shrif",
                "email": "ahmad.shrif@gmail.com"
            },
            "capabilities": {
                "databases_supported": "39+ NCBI databases including PubMed, Protein, Gene, Nucleotide, and more",
                "eutils_supported": [
                    "ESearch - Search databases for records matching a query",
                    "EFetch - Retrieve full records from NCBI databases by ID",
                    "ESummary - Get document summaries with key metadata",
                    "ELink - Find related records across NCBI databases", 
                    "EPost - Upload ID lists to NCBI history server",
                    "EInfo - Get database information and search fields",
                    "EGQuery - Search all NCBI databases simultaneously",
                    "ESpell - Get spelling suggestions for search terms",
                    "ECitMatch - Match citations to PubMed IDs"
                ],
                "special_features": [
                    "Combined search and fetch operations",
                    "Rate limiting (3 req/sec without API key, 10 req/sec with)",
                    "NCBI history server support for large datasets",
                    "Comprehensive error handling",
                    "Command line interface"
                ]
            },
            "use_cases": [
                "Biomedical literature search and analysis",
                "Protein and gene sequence retrieval",
                "Citation matching and bibliography management",
                "Cross-database linking and discovery",
                "Spell checking for scientific terms",
                "Large-scale bioinformatics data processing"
            ],
            "technical_details": {
                "protocol": "Model Context Protocol (MCP)",
                "architecture": "Modular design with 5 focused components",
                "built_on": "Robust ncbi-client package",
                "python_requirement": ">=3.9",
                "dependencies": ["mcp>=1.0.0", "click>=8.0.0", "ncbi-client"]
            },
            "getting_started": {
                "installation": "pip install -e .",
                "start_server": "ncbi-mcp serve",
                "test_connection": "ncbi-mcp test",
                "list_tools": "ncbi-mcp list-tools",
                "example_search": "Search PubMed: esearch(db='pubmed', term='cancer therapy', retmax=5)"
            }
        }
        
        return json.dumps(server_info, indent=2)
    
    def dispatch(self, name: str, arguments: Dict[str, Any]) -> str:
        """Dispatch tool call to appropriate handler."""
        handlers = {
            "esearch": self.handle_esearch,
            "efetch": self.handle_efetch,
            "esummary": self.handle_esummary,
            "epost": self.handle_epost,
            "elink": self.handle_elink,
            "einfo": self.handle_einfo,
            "egquery": self.handle_egquery,
            "espell": self.handle_espell,
            "ecitmatch": self.handle_ecitmatch,
            "search_and_fetch": self.handle_search_and_fetch,
            "get_databases": self.handle_get_databases,
            "server_info": self.handle_server_info,
        }
        
        handler = handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")
        
        return handler(arguments)


# Global handlers instance
tool_handlers = NCBIToolHandlers()
