from langchain_tavily import TavilySearch
import os
def handle(event, context):
    """
    Lambda function handler to process search requests.
    
    Args:
        event (dict): The event data containing search parameters.
        context (object): The context object provided by AWS Lambda.
        
    Returns:
        dict: The response containing search results.
    """
    try:
        os.environ['TAVILY_API_KEY'] = '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'  # Replace with your actual API key
        search = TavilySearch(
            max_results=5,
            include_images=True,
            topic="general",

        )
        results = search.invoke({'query': event.get('query', 'default search query')})
        return {
            "statusCode": 200,
            "body": results
        }
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }
    
