from langchain_tavily import TavilySearch
import os, json
def handler(event, context):
    """
    Lambda function handler to process search requests.
    
    Args:
        event (dict): The event data containing search parameters.
        context (object): The context object provided by AWS Lambda.
        
    Returns:
        dict: The response containing search results.
    """
    try:
        
        search = TavilySearch(
            max_results=5,
            include_images=True,
            topic="general",

        )
        results = search.invoke({'query': event.get('inputText', 'default search query')})
        actionGroup = event.get('actionGroup', None)
        fnc = event.get('function', None)
        print(event)
        print(actionGroup)
        print(results)
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup" : actionGroup,
                "function" : fnc,                
                "functionResponse" : {
                   
                   "responseBody" : {
                      "TEXT": {
                         "body": json.dumps(results)
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
    
