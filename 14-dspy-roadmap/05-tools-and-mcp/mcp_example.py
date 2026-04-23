# 05 — MCP integration sketch (commented; needs an MCP server).
#
# This file is a TEMPLATE. Adapt it once you have an MCP server running.
# The official server list is at https://github.com/modelcontextprotocol/servers
#
# Example MCP servers you might run:
#   - mcp-server-filesystem        (read/write files)
#   - mcp-server-github            (issues, PRs, repos)
#   - mcp-server-postgres          (query a Postgres DB)
#   - mcp-server-puppeteer         (drive a browser)
#
# Pick one, install it, run it on a port, then uncomment + adapt below.

"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import dspy


async def run():
    lm = dspy.LM("ollama_chat/qwen2.5-coder:7b", api_base="http://localhost:11434")
    dspy.configure(lm=lm)

    # 1. Connect to a stdio-based MCP server (e.g. the filesystem server).
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Discover the tools the server exposes.
            tools_resp = await session.list_tools()
            mcp_tools = tools_resp.tools

            # 3. Wrap each MCP tool as a dspy.Tool. (DSPy v3 has helpers for this;
            #    in older versions you'd write a small adapter.)
            dspy_tools = [
                dspy.Tool.from_mcp_tool(t, session=session) for t in mcp_tools
            ]

            # 4. Build a ReAct agent with the discovered tools.
            agent = dspy.ReAct("question -> answer", tools=dspy_tools, max_iters=4)
            result = agent(question="List the files in /tmp.")
            print(result.answer)


if __name__ == "__main__":
    asyncio.run(run())
"""
