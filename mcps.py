import os
from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP
mcp = FastMCP("simple-mcp")

# --- Your Tools ---
@mcp.tool()
def state_capital_f(state: str) -> str:
    """Provides the most up-to-date capital for a given US state."""
    capitals = {"Michigan": "Lansing", "Florida": "Tallahassee", "California": "Sacramento"}
    return capitals.get(state, "Unknown")

@mcp.tool()
def temperature_f(city: str) -> int:
    """Provides historical average temperature."""
    temps = {"Lansing": 50, "Tallahassee": 90, "Sacramento": 85}
    return temps.get(city, "Data not available")

# 2. Create the ASGI app (this is the magic line)
# This automatically creates the /sse and /messages endpoints
app = mcp.http_app()

if __name__ == "__main__":
    import uvicorn
    # Render assigns a port via the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    # Bind to 0.0.0.0 so Render's network can see the app
    uvicorn.run(app, host="0.0.0.0", port=port)
