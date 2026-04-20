import os
from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

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
    return temps.get(city, 0)

# 2. Create the FastAPI app
app = FastAPI()
sse = SseServerTransport("/messages")

@app.get("/")
async def root():
    return {"status": "MCP Server Running"}

@app.get("/sse")
async def handle_sse(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read, write):
        await mcp.server.run(read, write, mcp.server.create_initialization_options())

@app.post("/messages")
async def handle_messages(request: Request):
    await sse.handle_post_message(request.scope, request.receive, request._send)
