from flask import Flask, request
from pymessenger import Bot
#from chatutils import witResponse, getNews
from wit import Wit
from newsapi import NewsApiClient
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

newsapiKey = "b777c70da09e4280b7ba31563ea5ecd9"
witAccess = "VJK6OXA2NFJVVW4LNAS2U6NKCHWJJXDG"

newsClient = NewsApiClient(newsapiKey)
witClient = Wit(access_token=witAccess)

bot = Bot(ACCESS_TOKEN)

def witResponse(message):
    # Getting the response from the wit
    response = witClient.message(message)
    entities = response['entities']
    output = {"category": None, "location": None}
    for entity in entities:
        output[entity] = entities[entity][0]['value']  # getting the value
    return output

def getNews(query):
    elements = []
    try:
        location = query['location'].lower()
        category = query['category'].lower()
        headlines = newsClient.get_top_headlines(
            q=location, category=category, page_size=5)

        # extracting title,imageurl and url of the news
        # check facebook developers page for the format
        for item in headlines['articles']:
            element = {
                "title": item['title'],
                "image_url": item['urlToImage'],
                "buttons": [{
                    'type': 'web_url',
                    'title': 'Read More',
                    'url': item['url']
                }]
            }
            elements.append(element)

    except:
        element = {
            "title": 'Sorry!! I am still learning',
            "image_url": 'https://cdn.pixabay.com/photo/2013/07/13/13/36/android-161184_960_720.png',
            "buttons": [{
                'type': 'web_url',
                'title': 'Read More',
                'url': 'https://domain.com'
            }]
        }
        elements.append(element)
    return elements

# check for the document in webhook facebook verification
@app.route('/')
def index():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification Failed", 403
        return request.args["hub.challenge"], 200
    return "<html><body><h3><marquee>Hello World!!!</marquee></h3></body></html>", 200


@app.route('/', methods=['POST'])
def message():
    data = request.get_json()
    # print(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                senderId = messaging_event['sender']['id']
                recipientId = messaging_event['recipient']['id']
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        message = messaging_event['message']['text']
                    else:
                        message = 'no message'
                    #response = "you said " + message
                    response = getNews(witResponse(message))
                    # bot.send_text_message(senderId,"response")
                    bot.send_generic_message(senderId, response)
    print(senderId, recipientId, response)
    return "HI", 200


if __name__ == "__main__":
    app.run(debug=True)

# Facebook Authentication
#
