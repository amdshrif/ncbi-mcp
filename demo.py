#!/usr/bin/env python3
"""
Demo script showing NCBI MCP Server capabilities for a research workflow.
"""

import sys
import json
import time

# Import the refactored handlers
from src.ncbi_mcp.handlers import tool_handlers

def demo_literature_search():
    """Demonstrate a literature search workflow."""
    print("🔬 DEMO: Literature Search for COVID-19 Vaccine Research")
    print("=" * 60)
    
    # Search for COVID-19 vaccine papers
    print("1. Searching for recent COVID-19 vaccine research...")
    search_result = tool_handlers.handle_esearch({
        "db": "pubmed",
        "term": "COVID-19 vaccine effectiveness",
        "retmax": 10,
        "mindate": "2023/01/01",
        "maxdate": "2024/12/31",
        "sort": "pub_date"
    })
    
    search_data = json.loads(search_result)
    print(f"   Found {search_data.get('count', 0)} total articles")
    print(f"   Retrieved top 10 PMIDs: {search_data.get('id_list', [])}")
    
    time.sleep(0.5)
    
    # Get summaries for the top articles
    print("\n2. Getting summaries for top articles...")
    if search_data.get('id_list'):
        summary_result = tool_handlers.handle_esummary({
            "db": "pubmed",
            "id_list": search_data['id_list'][:3]
        })
        
        summary_data = json.loads(summary_result)
        print(f"   Retrieved {len(summary_data.get('docsums', []))} article summaries")
        
        # Show first article details
        if summary_data.get('docsums'):
            first_article = summary_data['docsums'][0]
            print(f"   📄 First article: {first_article.get('title', 'No title')}")
            print(f"      Authors: {', '.join(first_article.get('authors', [])[:3])}...")
            print(f"      Journal: {first_article.get('source', 'Unknown')}")
            print(f"      Date: {first_article.get('pubdate', 'Unknown')}")
    
    time.sleep(0.5)

def demo_protein_research():
    """Demonstrate protein research workflow."""
    print("\n🧬 DEMO: Protein Research - Insulin Studies")
    print("=" * 60)
    
    # Search for insulin protein entries
    print("1. Searching for human insulin protein sequences...")
    search_result = tool_handlers.handle_esearch({
        "db": "protein",
        "term": "insulin[protein] AND human[organism]",
        "retmax": 5
    })
    
    search_data = json.loads(search_result)
    print(f"   Found {search_data.get('count', 0)} protein entries")
    print(f"   Retrieved IDs: {search_data.get('id_list', [])}")
    
    time.sleep(0.5)
    
    # Get protein summaries
    if search_data.get('id_list'):
        print("\n2. Getting protein sequence information...")
        summary_result = tool_handlers.handle_esummary({
            "db": "protein",
            "id_list": search_data['id_list'][:2]
        })
        
        summary_data = json.loads(summary_result)
        if summary_data.get('docsums'):
            first_protein = summary_data['docsums'][0]
            print(f"   🧬 Protein: {first_protein.get('title', 'No title')}")
            print(f"      Length: {first_protein.get('length', 'Unknown')} amino acids")
            print(f"      Organism: {first_protein.get('organism', 'Unknown')}")
    
    time.sleep(0.5)

def demo_combined_search():
    """Demonstrate the combined search and fetch tool."""
    print("\n📚 DEMO: Combined Search & Fetch - Cancer Immunotherapy")
    print("=" * 60)
    
    print("1. Performing combined search and fetch for cancer immunotherapy abstracts...")
    
    result = tool_handlers.handle_search_and_fetch({
        "db": "pubmed",
        "term": "cancer immunotherapy checkpoint inhibitors",
        "retmax": 3,
        "rettype": "abstract",
        "retmode": "text"
    })
    
    print(f"   📄 Retrieved {len(result.split('PMID:')) - 1} abstracts")
    
    # Show a preview of the first abstract
    lines = result.split('\n')
    preview_lines = []
    for line in lines[:15]:  # First 15 lines
        if line.strip():
            preview_lines.append(line)
    
    print("   Preview of results:")
    for line in preview_lines[:10]:
        print(f"      {line}")
    print("      ...")

def demo_database_exploration():
    """Demonstrate database exploration capabilities."""
    print("\n🗄️ DEMO: NCBI Database Exploration")
    print("=" * 60)
    
    # Get all available databases
    print("1. Exploring available NCBI databases...")
    db_result = tool_handlers.handle_get_databases({})
    db_data = json.loads(db_result)
    
    print(f"   📊 Total databases available: {db_data['count']}")
    print("   🔬 Key biological databases:")
    
    key_dbs = ['pubmed', 'protein', 'nuccore', 'gene', 'genome', 'pmc', 'sra']
    available_key_dbs = [db for db in key_dbs if db in db_data['available_databases']]
    
    for db in available_key_dbs:
        print(f"      • {db}")
    
    print(f"   📝 Other available databases: {len(db_data['available_databases']) - len(available_key_dbs)} more")

def main():
    """Run all demos."""
    print("🚀 NCBI MCP Server - Research Capabilities Demo")
    print("This demonstrates what an LLM could do with NCBI data access")
    print("=" * 70)
    
    # Run all demos
    demo_literature_search()
    demo_protein_research()
    demo_combined_search()
    demo_database_exploration()
    
    print("\n" + "=" * 70)
    print("✨ Demo completed! The NCBI MCP Server enables LLMs to:")
    print("   • Search scientific literature across PubMed")
    print("   • Access protein and nucleotide sequence databases")
    print("   • Retrieve detailed abstracts and metadata")
    print("   • Explore relationships between biological entities")
    print("   • Perform complex multi-step research workflows")
    print("   • Access all 39+ NCBI databases programmatically")
    print("\n🎯 This provides comprehensive biological research capabilities!")

if __name__ == "__main__":
    main()
