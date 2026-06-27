from mcp.server.fastmcp import FastMCP

mcp = FastMCP("left_brain")


@mcp.tool()
def analyze_hijack_risk(vehicle_id: str, status: str) -> str:
    """Analyzes vehicle status to determine if a lockdown is needed."""
    if status == "THREAT_DETECTED":
        return f"CRITICAL: Hijack risk confirmed for {vehicle_id}. Initiating immobilization protocols."
    else:
        return f"Status normal for {vehicle_id}."


if __name__ == "__main__":
    mcp.run()
