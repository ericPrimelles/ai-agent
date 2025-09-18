from langchain_mcp_adapters.client import MultiServerMCPClient 

client = MultiServerMCPClient(
    {
        'web_search' : {
            'transport' : 'stdio',
            'command' : 'python',
            'args': ['src/mcp_tools/web_search.py'],
        }
    }
)

async def get_tools():
    return await client.get_tools()