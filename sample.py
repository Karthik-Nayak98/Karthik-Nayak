from flask import Flask, request
from pymessenger import Bot
from chatutils import witResponse, getNews

app = Flask(__name__)

fbAccessToken = "EAAL8jQoSZAcwBAIIhOvZCwWRzH2PSjegCo0xuZBZAuc0UPDO2BLgDuZBvQ3DgHBaLXizPCakJ1v4iQteZBzOI2QGj4cl9dQmFi8PdZCk9GdfwghzOzKcUshJAOIZAjoO7mkIvvu363Sd0K4WUZBpAueBvoOe0XZCXPnlQHwWtzsCtcZC8GZCjwJ2FXVO"

bot = Bot(fbAccessToken)
# check for the document in webhook facebook verification
@app.route('/')
def index():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "process.env.VERIFICATION_TOKEN":
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
