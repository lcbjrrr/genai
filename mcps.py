import os
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

mcp = FastMCP("simple-mcp")

@mcp.tool()
def state_capital_f(state: str) -> str:
    """Provides the most up-to-date capital for a given US state."""
    state_capital_dict = {"Michigan": "Lansing", "Florida": "Tallahassee", "California": "Sacramento", "Texas": "Austin", "New York": "Albany"}
    return state_capital_dict.get(state, "Unknown")

@mcp.tool()
def temperature_f(city: str) -> int:
    """Provides the historical average temperature for a given city."""
    temp_dict = {"Lansing": 50, "Tallahassee": 90, "Sacramento": 85, "Austin": 80, "Albany": 45}
    return temp_dict.get(city, "Data not available")

# --- THE RENDER FIX ---
# Manually create the Starlette app that Render can talk to
sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await mcp.server.run(read_stream, write_stream, mcp.server.create_initialization_options())

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

# This is the "app" object Render will look for
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)
