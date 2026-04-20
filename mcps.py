import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("simple-mcp")

@mcp.tool()
def state_capital_f(state: str) -> str:
    """Provides the most up-to-date capital for a given US state."""
    state_capital_dict = {
        "Michigan": "Lansing", "Florida": "Tallahassee", "California": "Sacramento",
        "Texas": "Austin", "New York": "Albany"
    }
    return state_capital_dict.get(state, "Unknown")

@mcp.tool()
def temperature_f(city: str) -> int:
    """Provides the historical average temperature for a given city."""
    temp_dict = {"Lansing": 50, "Tallahassee": 90, "Sacramento": 85, "Austin": 80, "Albany": 45}
    return temp_dict.get(city, "Data not available")

if __name__ == "__main__":
    # Get the port Render assigned
    port = int(os.environ.get("PORT", 10000))
    
    # OFFICIAL way to run FastMCP as a web server on Render
    # This automatically sets up the /sse and /messages endpoints
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=port
    )
