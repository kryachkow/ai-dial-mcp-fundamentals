import asyncio
import os

from agent.dial_client import DialClient
from agent.mcp_client import MCPClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

async def main():
    # TODO:
    # 1. Create MCP client and open connection to the MCP server (use `async with {YOUR_MCP_CLIENT} as mcp_client`),
    #    mcp_server_url="http://localhost:8005/mcp"
    # 2. Get Available MCP Resources and print them
    # 3. Get Available MCP Tools, assign to `tools` variable, print tool as well
    # 4. Create DialClient
    # 5. Create list with messages and add there SYSTEM_PROMPT with instructions to LLM
    # 6. Add to messages Prompts from MCP server as User messages
    # 7. Create console chat (infinite loop + ability to exit from chat + preserve message history after the call to dial client)
    async with MCPClient(mcp_server_url="http://localhost:8005/mcp") as mcp_client:
        print("Resources: ")
        print(await mcp_client.get_resources())
        tools = await mcp_client.get_tools()
        print("Tools: ")
        client = DialClient(api_key=os.getenv('DIAL_API_KEY', ''), endpoint='https://ai-proxy.lab.epam.com',
                            mcp_client=mcp_client, tools=tools)
        prompts = await mcp_client.get_prompts()
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]
        for prompt in prompts:
            messages.append(Message(role=Role.USER, content=prompt.description))

        while True:
            user_message = input(">")
            messages.append(Message(role=Role.USER, content=user_message))
            ai_message = await client.get_completion(messages)
            print("AI response: " + ai_message.content)
            messages.append(ai_message)


if __name__ == "__main__":
    asyncio.run(main())
