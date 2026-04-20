from mcp.server.fastmcp import FastMCP

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

if __name__ == "__main__":
    mcp.run(transport="sse")
