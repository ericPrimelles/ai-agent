import requests, os

def handler(event, context):
    try:
        url = os.env.get('ALB_DNS')
        urls = event.get('urls')
        result = requests.post(url, json=urls)
        return result.json()
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }
    