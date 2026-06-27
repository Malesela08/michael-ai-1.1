import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run():
    # Connect to the running left_brain server
    server_params = StdioServerParameters(
        command="python3", args=["left_brain/server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Send a test command to the brain
            result = await session.call_tool(
                "process_data", arguments={"data": "Hello Brain!"}
            )
            print(f"Result from Left Brain: {result}")


if __name__ == "__main__":
    asyncio.run(run())
