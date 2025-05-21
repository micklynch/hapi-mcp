import sseclient
import requests
import time

try:
    url = 'http://localhost:8000/sse' 
    print(f"Attempting to connect to {url}")
    
    # Use requests.get with stream=True and Accept header
    response = requests.get(url, stream=True, headers={'Accept': 'text/event-stream'}, timeout=10)
    print(f"Response status code: {response.status_code}")
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    
    content_type = response.headers.get('Content-Type', '').lower()
    print(f"Response Content-Type: {content_type}")

    if 'text/event-stream' not in content_type:
        print("Warning: Response Content-Type is not 'text/event-stream'. SSE client may not work as expected.")
        # Depending on strictness, one might choose to exit here.
        # For now, let's still try to pass it to SSEClient to see what happens.

    messages = sseclient.SSEClient(response)
    print(f"SSEClient initialized. Waiting for messages...")
    
    first_message_received = False
    for msg in messages: # This is where the TypeError has been occurring
        print(f"Received event: type='{msg.event}', data='{msg.data}'")
        first_message_received = True
        break 
    
    # messages.close() # SSEClient with requests.Response doesn't have a close method.

    if first_message_received:
        print("Connection successful and at least one message received.")
    else:
        print("Connection likely successful (if no error during iteration), but no messages received from the server during the listening period.")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e.response.status_code}")
    if e.response.status_code == 404:
        print(f"The endpoint {url} was not found.")
    else:
        print(f"A non-404 HTTP error occurred: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")
except requests.exceptions.ReadTimeout:
    print(f"Connection to {url} timed out.")
except TypeError as e:
    print(f"TypeError encountered: {e}. This often means the SSEClient object was not iterable.")
    print("This could be due to an incorrect server response (e.g., wrong Content-Type) or an issue with the client library/usage.")
except Exception as e:
    print(f"An unexpected error occurred: {type(e).__name__} - {e}")
finally:
    # Ensure the response is closed if it was opened, especially if not iterated fully.
    if 'response' in locals() and hasattr(response, 'close'):
        response.close()
        print("Closed the response stream.")
