import asyncio
import json
import os

from agent.mcp_client import MCPClient
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


async def main():

    #TODO:
    # 1. Create MCP client with `docker_image="mcp/duckduckgo:latest"` as `mcp_client`
    # 2. Get Available MCP Tools, assign to `tools` variable, print tool as well
    # 3. Create DialClient:
    #       - api_key=os.getenv("DIAL_API_KEY")
    #       - endpoint="https://ai-proxy.lab.epam.com"
    #       - tools=tools
    #       - mcp_client=mcp_client
    # 4. Create list with messages and add there SYSTEM_PROMPT with instructions to LLM
    # 5. Create console chat (infinite loop + ability to exit from chat + preserve message history after the call to dial client)
    async with MCPClient(docker_image="mcp/duckduckgo:latest") as mcp_client:
        tools = await  mcp_client.get_tools()

        print(json.dumps(tools, indent=2))
        client = DialClient(api_key=os.getenv("DIAL_API_KEY"), endpoint="https://ai-proxy.lab.epam.com", tools=tools,
                            mcp_client=mcp_client)
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

        while True:
            user_message = input(">")
            messages.append(Message(role=Role.USER, content=user_message))
            ai_message = await client.get_completion(messages)
            print("AI response: " + ai_message.content)
            messages.append(ai_message)


if __name__ == "__main__":
    asyncio.run(main())