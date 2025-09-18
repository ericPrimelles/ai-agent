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
        response = await self.agent.arun(input=input_text)
        return response
    
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='../../.env') 
    async def main():
        agent = ComparablesAgent(model_name="gpt-4")
        await agent.setup()
        test_input = "comparables: 123 Main St, Miami, FL, 33333"
        response = await agent.run(test_input)
        print(response)

    asyncio.run(main())