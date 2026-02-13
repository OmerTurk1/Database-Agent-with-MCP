import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from client import send_to_model

async def run_bot():
    server_script = os.path.abspath("server.py")
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
        env=os.environ.copy()
    )

    messages = [
        {"role": "system", "content": "You are an MCP agent and you control a Sqlite database. If necessary, use a tool."}
    ]

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Start Server and list tools
            await session.initialize()
            available_tools = await session.list_tools()
            # Prepare appropriate tool schemas for LLM format
            tools_for_llm = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                } for tool in available_tools.tools
            ]

            print("--- Database Management Bot is Active! ---")

            while True:
                # Take the input in asencron loop
                user_input = await asyncio.to_thread(input, "\n>>>(Press q to quit): ")
                if user_input.lower()=="q": break
                
                messages.append({"role": "user", "content": user_input})

                while True:
                    # call the model together with tool definitions
                    response = send_to_model(messages, tools_for_llm)
                    message = response.choices[0].message

                    if message.tool_calls:
                        messages.append(message)

                        for call in message.tool_calls:
                            tool_name = call.function.name
                            args = json.loads(call.function.arguments)

                            print(f"[*] Tool is called: {tool_name}...")
                            
                            # CRITICAL POINT: Call tool on MCP Server
                            result = await session.call_tool(tool_name, arguments=args)
                            extracted_content = "\n".join([c.text for c in result.content if hasattr(c, 'text')])

                            messages.append({
                                "role": "tool",
                                "tool_call_id": call.id,
                                "content": extracted_content
                            })
                    else:
                        print(f"\nBot: {message.content}")
                        messages.append(message)
                        break

if __name__ == "__main__":
    asyncio.run(run_bot())