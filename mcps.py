from mcp.server.fastmcp import FastMCP
import os
from starlette.responses import JSONResponse

mcp = FastMCP("simple-mcp")

@mcp.tool()
def state_capital_f(state: str) -> str:
    """Provides the most up-to-date capital for a given US state."""
    state_capital_dict = {
        "Michigan": "Lansing",
        "Florida": "Tallahassee",
        "California": "Sacramento",
        "Texas": "Austin",
        "New York": "Albany"
    }
    capital = state_capital_dict.get(state, "Unknown")
    print(f"------> {state}: {capital}")
    return capital

@mcp.tool()
def temperature_f(city: str) -> int:
    """Provides the historical average temperature for a given city."""
    temp_dict = {
        "Lansing": 50,
        "Tallahassee": 90,
        "Sacramento": 85,
        "Austin": 80,
        "Albany": 45
    }
    temp = temp_dict.get(city, "Data not available")
    print(f"=====> {city}: {temp}")
    return temp

@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    return JSONResponse({"status": "ok"})[web:19]

if __name__ == "__main__":
    app = mcp.http_app()  # ASGI app for /mcp endpoint
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
