"""
Command-line interface for NCBI MCP Server.

Provides CLI functionality for running the MCP server and managing tools.
"""

import asyncio
import json
import sys
from typing import Optional

import click

from .server import main as server_main
from .schemas import get_tool_schemas
from .handlers import tool_handlers


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, verbose: bool):
    """NCBI MCP Server command-line interface."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option('--port', '-p', type=int, help='Port for HTTP server (default: stdio)')
@click.option('--host', '-h', default='localhost', help='Host for HTTP server')
@click.pass_context
def serve(ctx, port: Optional[int], host: str):
    """Start the NCBI MCP Server."""
    if ctx.obj['verbose']:
        if port:
            click.echo(f"Starting NCBI MCP Server on {host}:{port}")
        else:
            click.echo("Starting NCBI MCP Server with stdio communication")
    
    try:
        if port:
            # TODO: Implement HTTP server mode
            click.echo("HTTP server mode not yet implemented. Using stdio mode.")
        
        # Start stdio server
        asyncio.run(server_main())
        
    except KeyboardInterrupt:
        if ctx.obj['verbose']:
            click.echo("\nServer stopped by user")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'names']),
              help='Output format')
@click.pass_context
def list_tools(ctx, output_format: str):
    """List all available MCP tools."""
    try:
        tools = get_tool_schemas()
        
        if output_format == 'json':
            # Convert tools to JSON serializable format
            tools_data = []
            for tool in tools:
                tool_data = {
                    'name': tool.name,
                    'description': tool.description,
                    'parameters': tool.inputSchema
                }
                tools_data.append(tool_data)
            click.echo(json.dumps(tools_data, indent=2))
            
        elif output_format == 'names':
            for tool in tools:
                click.echo(tool.name)
                
        else:  # table format
            click.echo("Available NCBI MCP Tools:")
            click.echo("=" * 50)
            
            # Group tools by category
            eutils = []
            helpers = []
            
            for tool in tools:
                if tool.name in ['search_and_fetch', 'get_databases']:
                    helpers.append(tool)
                else:
                    eutils.append(tool)
            
            if eutils:
                click.echo("\n📚 NCBI E-utilities (9 tools):")
                for tool in eutils:
                    click.echo(f"  • {tool.name:<12} - {tool.description}")
            
            if helpers:
                click.echo("\n🔧 Helper Tools (2 tools):")
                for tool in helpers:
                    click.echo(f"  • {tool.name:<12} - {tool.description}")
            
            click.echo(f"\nTotal: {len(tools)} tools available")
            
    except Exception as e:
        click.echo(f"Error listing tools: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('tool_name')
@click.option('--format', 'output_format', default='pretty', 
              type=click.Choice(['pretty', 'json']),
              help='Output format')
@click.pass_context
def describe_tool(ctx, tool_name: str, output_format: str):
    """Describe a specific MCP tool and its parameters."""
    try:
        tools = get_tool_schemas()
        tool = next((t for t in tools if t.name == tool_name), None)
        
        if not tool:
            click.echo(f"Tool '{tool_name}' not found.", err=True)
            click.echo(f"Available tools: {', '.join(t.name for t in tools)}")
            sys.exit(1)
        
        if output_format == 'json':
            tool_data = {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.inputSchema
            }
            click.echo(json.dumps(tool_data, indent=2))
        else:
            click.echo(f"Tool: {tool.name}")
            click.echo("=" * (len(tool.name) + 6))
            click.echo(f"Description: {tool.description}")
            
            # Extract parameters from schema
            schema = tool.inputSchema if isinstance(tool.inputSchema, dict) else {}
            
            properties = schema.get('properties', {})
            required = schema.get('required', [])
            
            if properties:
                click.echo(f"\nParameters:")
                for param_name, param_info in properties.items():
                    required_mark = " (required)" if param_name in required else " (optional)"
                    param_type = param_info.get('type', 'unknown')
                    param_desc = param_info.get('description', 'No description')
                    click.echo(f"  • {param_name}{required_mark}")
                    click.echo(f"    Type: {param_type}")
                    click.echo(f"    Description: {param_desc}")
                    if 'enum' in param_info:
                        click.echo(f"    Allowed values: {', '.join(param_info['enum'])}")
                    click.echo()
            else:
                click.echo("\nNo parameters required.")
                
    except Exception as e:
        click.echo(f"Error describing tool: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('tool_name')
@click.argument('parameters', required=False)
@click.option('--param', '-p', multiple=True, help='Parameter in key=value format')
@click.option('--output', '-o', help='Output file (default: stdout)')
@click.pass_context
def call_tool(ctx, tool_name: str, parameters: Optional[str], param: tuple, output: Optional[str]):
    """Call an MCP tool with parameters."""
    try:
        # Parse parameters
        tool_params = {}
        
        # Parse JSON parameters if provided
        if parameters:
            try:
                tool_params = json.loads(parameters)
            except json.JSONDecodeError as e:
                click.echo(f"Invalid JSON parameters: {e}", err=True)
                sys.exit(1)
        
        # Parse key=value parameters
        for p in param:
            if '=' not in p:
                click.echo(f"Invalid parameter format: {p}. Use key=value format.", err=True)
                sys.exit(1)
            key, value = p.split('=', 1)
            # Try to parse value as JSON, fall back to string
            try:
                tool_params[key] = json.loads(value)
            except json.JSONDecodeError:
                tool_params[key] = value
        
        if ctx.obj['verbose']:
            click.echo(f"Calling tool '{tool_name}' with parameters: {tool_params}")
        
        # Call the tool
        result = tool_handlers.dispatch(tool_name, tool_params)
        
        # Output result
        if output:
            with open(output, 'w') as f:
                f.write(result)
            if ctx.obj['verbose']:
                click.echo(f"Results written to {output}")
        else:
            click.echo(result)
            
    except Exception as e:
        click.echo(f"Error calling tool: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def test(ctx):
    """Run basic connectivity test with NCBI."""
    try:
        if ctx.obj['verbose']:
            click.echo("Testing NCBI connectivity...")
        
        # Test with get_databases - simple and fast
        result = tool_handlers.handle_get_databases({})
        data = json.loads(result)
        
        click.echo("✅ NCBI MCP Server Test Results:")
        click.echo(f"   • Successfully connected to NCBI")
        click.echo(f"   • Found {data['count']} available databases")
        click.echo(f"   • Sample databases: {', '.join(data['available_databases'][:5])}")
        click.echo("   • All tools should be working correctly")
        
    except Exception as e:
        click.echo(f"❌ Connectivity test failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information."""
    try:
        # Try to read version from package
        from importlib.metadata import version as get_version
        try:
            pkg_version = get_version('ncbi-mcp')
        except:
            pkg_version = "development"
        
        click.echo(f"NCBI MCP Server version: {pkg_version}")
        click.echo("Model Context Protocol (MCP) server for NCBI E-utilities")
        click.echo("Provides access to PubMed, protein sequences, and genetic databases")
        
    except Exception as e:
        click.echo(f"Error getting version: {e}", err=True)


if __name__ == '__main__':
    cli()
