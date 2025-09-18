from langchain_mcp_adapters.client import MultiServerMCPClient 
from pathlib import Path

path = Path(__file__).parent.parent.parent
print('Path:', path)
client = MultiServerMCPClient(
    {
        'web_search' : {
            'transport' : 'stdio',
            'command' : 'python',
            'args': [f'{str(path)}/mcp_tools/web_search.py'],
        }
    }
)

async def get_tools():
    return await client.get_tools()