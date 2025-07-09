from langchain_tavily import TavilySearch
import os, json


def scrapper(event, context):
    try:
        print(event)
        url = os.getenv('ALB_DNS')
        urls = event.get('urls')
        body = {"urls" : urls}
        result = requests.post(f'http://{url}/scrapper', json=body)
        return result.json()
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }

def get_query(event):
    parameters = event.get('parameters', [])
    for p in parameters:
        if p['name'] == 'query':
            return p['value'] 
        
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
        results = search.invoke({'query': get_query(event)})
        actionGroup = event.get('actionGroup', None)
        fnc = event.get('function', None)
        print(event)
        print(actionGroup)
        print(results)
        data = results.get('results', [])
        urls = [d.get('url') for d in data if d.get('url') ]
        enrichment = scrapper(urls)

        final_result = {
            'images' : results.get('images', []),
            'search_result' : results.get('results', []),
            'enriched_data' : enrichment
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
    
