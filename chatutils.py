from wit import Wit
from newsapi import NewsApiClient

newsapiKey = "b777c70da09e4280b7ba31563ea5ecd9"
witAccess = "VJK6OXA2NFJVVW4LNAS2U6NKCHWJJXDG"

newsClient = NewsApiClient(newsapiKey)
witClient = Wit(access_token=witAccess)

#witClient.message("What are the top sports news from India")


def witResponse(message):
    # Getting the response from the wit
    response = witClient.message(message)
    entities = response['entities']
    output = {"category": None, "location": None}
    for entity in entities:
        output[entity] = entities[entity][0]['value']  # getting the value
    return output

#witResponse("Give me the latest technology news from India")
#news = newsClient.get_top_headlines(q="India",category="general",page_size = 5)


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


#query = witResponse("Technology news India")
#sample = getNews(query)
# print(sample)
