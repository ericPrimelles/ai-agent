from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        'web_search' : {
            'transport' : 'stdio',
            'command' : 'python',
            'args': ['src/mcp_tools/web_search.py'],
        }
    }
)

tools = [client.get_tools()]
agent = create_agent(
    tools=tools,
    llm='gpt-4',
    
)
