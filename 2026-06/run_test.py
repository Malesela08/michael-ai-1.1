import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run():
    server_path = Path(__file__).resolve().parents[1] / "src" / "brain" / "left_brain" / "server.py"
    server_params = StdioServerParameters(
        command="python3", args=[str(server_path)]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "analyze_hijack_risk",
                arguments={"vehicle_id": "CAR-123", "status": "THREAT_DETECTED"},
            )
            print(f"Logic Response: {result}")


if __name__ == "__main__":
    asyncio.run(run())
