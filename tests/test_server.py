#!/usr/bin/env python3
"""
Test script for NCBI MCP Server to validate functionality.
"""

import sys
import json
import time
from typing import Dict, Any

# Import the refactored handlers
from src.ncbi_mcp.handlers import tool_handlers

def test_get_databases():
    """Test getting list of databases."""
    print("Testing get_databases...")
    try:
        result = tool_handlers.handle_get_databases({})
        data = json.loads(result)
        print(f"✓ Found {data['count']} databases")
        print(f"  First 5 databases: {data['available_databases'][:5]}")
        time.sleep(0.5)  # Rate limiting
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_einfo():
    """Test getting database info."""
    print("\nTesting einfo...")
    try:
        # Test getting all databases
        result = tool_handlers.handle_einfo({})
        data = json.loads(result)
        print(f"✓ Database list retrieved: {len(data['databases'])} databases")
        time.sleep(0.5)  # Rate limiting
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_esearch():
    """Test searching PubMed."""
    print("\nTesting esearch...")
    try:
        # Simple search
        result = tool_handlers.handle_esearch({
            "db": "pubmed",
            "term": "insulin",
            "retmax": 5
        })
        data = json.loads(result)
        print(f"✓ Search completed: {data.get('count', 0)} results found")
        print(f"  Retrieved IDs: {data.get('id_list', [])}")
        time.sleep(0.5)  # Rate limiting
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_esummary():
    """Test getting summaries."""
    print("\nTesting esummary...")
    try:
        # First do a search to get some IDs
        search_result = tool_handlers.handle_esearch({
            "db": "pubmed",
            "term": "insulin",
            "retmax": 2
        })
        search_data = json.loads(search_result)
        time.sleep(0.5)  # Rate limiting
        
        if search_data.get('id_list'):
            # Now get summaries
            result = tool_handlers.handle_esummary({
                "db": "pubmed",
                "id_list": search_data['id_list'][:2]
            })
            data = json.loads(result)
            print(f"✓ Summaries retrieved for {len(search_data['id_list'][:2])} articles")
            time.sleep(0.5)  # Rate limiting
            return True
        else:
            print("✗ No IDs from search to test summaries")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_efetch():
    """Test fetching records."""
    print("\nTesting efetch...")
    try:
        # Use a known PMID
        result = tool_handlers.handle_efetch({
            "db": "pubmed",
            "id_list": ["33946458"],  # A real PMID
            "rettype": "abstract",
            "retmode": "text"
        })
        
        if result and len(result) > 100:  # Abstract should be substantial
            print(f"✓ Abstract fetched: {len(result)} characters")
            print(f"  Preview: {result[:100]}...")
            time.sleep(0.5)  # Rate limiting
            return True
        else:
            print(f"✗ Unexpected result length: {len(result) if result else 0}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_dispatcher():
    """Test the tool dispatcher."""
    print("\nTesting dispatcher...")
    try:
        # Test via dispatcher
        result = tool_handlers.dispatch("get_databases", {})
        data = json.loads(result)
        print(f"✓ Dispatcher works: {data['count']} databases via dispatch")
        time.sleep(0.5)  # Rate limiting
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("NCBI MCP Server Test Suite (Refactored)")
    print("=" * 50)
    
    tests = [
        test_get_databases,
        test_einfo,
        test_esearch,
        test_esummary,
        test_efetch,
        test_dispatcher
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The refactored NCBI MCP Server is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
