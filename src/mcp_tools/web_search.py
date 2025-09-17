from mcp.server.fastmcp import FastMCP

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
        results = search.invoke({'query': get_query(event)})
        actionGroup = event.get('actionGroup', None)
        fnc = event.get('function', None)
        print(event)
        print(actionGroup)
        print(results)
        data = results.get('results', [])
        urls = [d.get('url') for d in data if d.get('url') ]
        #enrichment = scrapper({'urls': urls}, {})

        final_result = {
            'images' : results.get('images', []),
            'search_result' : results.get('results', []),
            #'enriched_data' : enrichment
            }
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup" : actionGroup,
                "function" : fnc,                
                "functionResponse" : {
                   
                   "responseBody" : {
                      "TEXT": {
                         "body": json.dumps(final_result)
                      }
                   }
                }
            }
        }
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }
    
