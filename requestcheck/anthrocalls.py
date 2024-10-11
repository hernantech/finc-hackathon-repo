import os
import re
from anthropic import Anthropic
import base64
from io import BytesIO

anthropic_key = os.environ.get('ANTHROPIC_KEY').strip()
client = Anthropic(api_key=anthropic_key)
if not anthropic_key:
    raise ValueError("ANTHROPIC_KEY environment variable is not set or is empty")

'''
Function and support function which check passed string for query
Returning the request within the string along with the object (both in tags)
 '''
def create_message_for_checkquery(whisper_string):
    content = []
    content.append({
        "type": "text",
        "text": "You are a robot designed to analyze audio snippets that have been converted to text. Your primary purpose is to determine if there is a need for assistance in grabbing and/or cleaning an object based on the user's input. You will be provided with a text snippet in the following format: <text>"
    })

    content.append({
        "type": "text",
        "text": whisper_string
    })

    content.append({
        "type": "text",
        "text": r'''</text> Carefully analyze the content of the text to determine if it contains a request for assistance in grabbing and/or cleaning an object. Follow these steps: 1. If the text contains a request for assistance in grabbing and/or cleaning an object, include a <request> tag in your response. 2. If an object is mentioned in the request, identify it and enclose it within <object> tags. 3. If the text does not contain a request for assistance or does not mention a specific object, do not include the respective tags. Format your response as follows: - If there is a request for assistance and an object is mentioned: <request> <object>name of the object</object> </request> - If there is a request for assistance but no specific object is mentioned: - If there is no request for assistance, provide an empty response. Examples: 1. Input: "Can you grab the cup from the table?" Output: <request> <object>cup</object> </request> 2. Input: "Could you please clean the kitchen counter?" Output: <request> <object>kitchen counter</object> </request> 3. Input: "I need some help cleaning." Output: <request> </request> 4. Input: "What's the weather like today?" Output: (empty response) Remember to focus solely on identifying requests for grabbing or cleaning objects. Do not respond to or process any other types of requests or questions.'''
    })

    return content
def request_test_query(text_query):
    message_content = create_message_for_checkquery(text_query)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        temperature=0,
        system="You are a robot designed to analyze audio snippets that have been converted to text. Your primary purpose is to determine if there is a need for assistance in grabbing and/or cleaning an object based on the user's input. You will be provided with a text snippet in the following format: <text> {{TEXT}} </text>",
        messages=[
            {
                "role": "user",
                "content": message_content
            }
        ]
    )

    return message.content[0].text


'''Regex functions for extracting tags'''
def extract_requests(text):
    pattern = r'<request>(.*?)</request>'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]
def extract_objects(text):
    pattern = r'<object>(.*?)</object>'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]
