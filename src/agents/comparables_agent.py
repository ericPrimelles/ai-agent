from mcp_clients.comparables_clients import get_tools
from models.openai import get_model
from prompts.comparables_agent.comparables import prompt
from langchain.agents import create_agent

class ComparablesAgent:
    def __init__(self, model_name: str):
        self.model = get_model(model_name)
        self.tools = None
        self.agent = None

    async def setup(self):
        self.tools = await get_tools()
        self.agent = create_agent(self.model, self.tools, prompt=prompt)

    async def run(self, input_text: str):
        if not self.agent:
            raise Exception("Agent not initialized. Call setup() before run().")
        response = await self.agent.ainvoke({"messages" : [{"role" : "user", "content" : input_text}]})
        return response
    
    
    async def stream(self, input_text: str):
        if not self.agent:
            raise Exception("Agent not initialized. Call setup() before run().")
        async for response in  self.agent.astream({"messages": [{"role": "user", "content": input_text}]}):
            yield response
    
if __name__ == "__main__":
    import asyncio, json
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='../../.env') 
    async def main():
        agent = ComparablesAgent(model_name="gpt-4")
        await agent.setup()
        test_input = "comparables: 123 Main St, Miami, FL, 33333"
        # Fix: Use async for instead of regular for
        async for chunk in agent.stream(test_input):
            print(chunk)
            input("Press Enter to continue...")
            # latest_message = chunk["messages"][-1]
            # if latest_message.content:
            #     print(f"Agent: {latest_message.content}")
            # elif latest_message.tool_calls:
            #     print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
        #json.dump(response['structured_response'], open('output.json', 'w'), indent=4)

    asyncio.run(main())