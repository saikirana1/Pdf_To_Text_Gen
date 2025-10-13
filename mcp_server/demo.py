import math
from mcp.server.fastmcp import FastMCP

# Create a FastMCP server named "Math"
mcp = FastMCP("Math")


# Tool: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Tool: Multiply two numbers
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


# Tool: Divide two numbers
@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b. Raises error if b is zero"""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
