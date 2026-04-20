import os
from mcp.server.fastmcp import FastMCP
from mcp.server.asgi import ASGIServer

# 1. Initialize FastMCP
mcp = FastMCP("simple-mcp")

# --- Your Tools (Keep as they are) ---
@mcp.tool()
def state_capital_f(state: str) -> str:
    """Provides the most up-to-date capital for a given US state."""
    capitals = {"Michigan": "Lansing", "Florida": "Tallahassee", "California": "Sacramento"}
    return capitals.get(state, "Unknown")

@mcp.tool()
def temperature_f(city: str) -> int:
    """Provides historical average temperature."""
    temps = {"Lansing": 50, "Tallahassee": 90, "Sacramento": 85}
    return temps.get(city, 0)

# 2. Wrap the MCP server in an ASGI app
# This creates the necessary web interface for Render
app = ASGIServer(mcp.server)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    # We must use 0.0.0.0 for Render to see the port
    uvicorn.run(app, host="0.0.0.0", port=port)
