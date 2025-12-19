import asyncio
from fastmcp import FastMCP
from asyncua import Client, ua
import logging

logging.basicConfig(level=logging.DEBUG)
# Set up logging
logger = logging.getLogger("opcua-mcp")
logger.setLevel(logging.DEBUG)

# Add file handler
file_handler = logging.FileHandler('opcua-mcp.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)


# Initialize FastMCP server
mcp = FastMCP("OPC UA MCP Server")

# OPC UA client connection
opcua_client = None
opcua_url = "opc.tcp://localhost:4840"

async def get_opcua_client():
    """Get or create OPC UA client connection"""
    global opcua_client
    if opcua_client is None:
        opcua_client = Client(opcua_url)
        await opcua_client.connect()
    return opcua_client


@mcp.tool()
async def connect_opcua(url: str) -> str:
    """Connect to an OPC UA server
    
    Args:
        url: OPC UA server URL (e.g., opc.tcp://localhost:4840)
    """
    global opcua_client, opcua_url
    try:
        if opcua_client:
            await opcua_client.disconnect()
        opcua_url = url
        opcua_client = Client(url)
        await opcua_client.connect()
        return f"Successfully connected to {url}"
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        return f"Failed to connect: {str(e)}"


@mcp.tool()
async def read_node(node_id: str) -> str:
    """Read value from an OPC UA node
    
    Args:
        node_id: Node ID (e.g., ns=2;i=2)
    """
    try:
        client = await get_opcua_client()
        node = client.get_node(node_id)
        value = await node.read_value()
        return f"Node {node_id} value: {value}"
    except Exception as e:
        logger.error(f"Read failed: {str(e)}")
        return f"Failed to read node: {str(e)}"


@mcp.tool()
async def write_node(node_id: str, value: float) -> str:
    """Write value to an OPC UA node
    
    Args:
        node_id: Node ID (e.g., ns=2;i=2)
        value: Value to write
    """
    try:
        client = await get_opcua_client()
        node = client.get_node(node_id)
        await node.write_value(ua.Variant(value, ua.VariantType.Float))
        node.write_value()
        return f"Successfully wrote '{value}' to node {node_id}"
    except Exception as e:
        logger.error(f"Write failed: {str(e)}")
        return f"Failed to write node: {str(e)}"


@mcp.tool()
async def browse_nodes(node_id: str = "i=84") -> str:
    """Browse child nodes of an OPC UA node
    
    Args:
        node_id: Parent node ID (default: i=84 for Objects folder)
    """
    try:
        client = await get_opcua_client()
        node = client.get_node(node_id)
        children = await node.get_children()
        
        result = f"Children of {node_id}:\n"
        for child in children:
            browse_name = await child.read_browse_name()
            result += f"  - {child.nodeid}: {browse_name.Name}\n"
        
        return result
    except Exception as e:
        logger.error(f"Browse failed: {str(e)}")
        return f"Failed to browse nodes: {str(e)}"


@mcp.tool()
async def disconnect_opcua() -> str:
    """Disconnect from the OPC UA server"""
    global opcua_client
    try:
        if opcua_client:
            await opcua_client.disconnect()
            opcua_client = None
            return "Disconnected from OPC UA server"
        return "No active connection"
    except Exception as e:
        logger.error(f"Disconnect failed: {str(e)}")
        return f"Failed to disconnect: {str(e)}"


if __name__ == "__main__":
    logger.info("Starting opcua-mcp server!")
    mcp.run()
