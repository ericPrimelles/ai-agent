from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch

mcp = FastMCP('web_search')

@mcp.tool()
def web_search(query: str) -> dict:
    """
    Lambda function handler to process search requests.
    
    Args:
        query (str): The event data containing search parameters.
        
    Returns:
        dict: The response containing search results.
    """
    try:
        
        search = TavilySearch(
            max_results=5,
            include_images=True,
            topic="general",

        )
        results = search.invoke({'query':query})
        data = results.get('results', [])
        urls = [d.get('url') for d in data if d.get('url') ]
        #enrichment = scrapper({'urls': urls}, {})

        return  {
            'images' : results.get('images', []),
            'search_result' : results.get('results', []),
            #'enriched_data' : enrichment
            }
        
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }
    
if __name__ == "__main__":
    mcp.run(transport='stdio')