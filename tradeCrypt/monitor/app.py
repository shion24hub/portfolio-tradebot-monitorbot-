from flask import (
    Flask,
    request,
    abort,
    render_template
)
from flask_httpauth import HTTPDigestAuth
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import config
import p

CHANNEL_ACCESS_TOKEN = config.CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET = config.CHANNEL_SECRET
API_SECRET = config.API_SECRET
ID_LIST = p.id_list

app = Flask(__name__)
app.config["SECRET_KEY"] = API_SECRET
auth = HTTPDigestAuth()

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@auth.get_password
def get_password(id) :
    if id in ID_LIST :
        return ID_LIST.get(id)
    return None

@app.route("/", methods=["POST"])
@auth.login_required
def index() :
    postedData = request.get_json(force=True)
    name = postedData["name"]
    etype = postedData["etype"]
    return """
    hi, {}. i'm here.
    
    posted data is below.
    name : {}
    etype : {}
    """.format(auth.username(), name, etype)

# @app.route("/api", methods=["POST"])
# def api() :
#     name = request.form["name"]

#     message = "postリクエストを受信しました。name : {}".format(name)
#     line_bot_api.push_message(
#         TEST_USER_ID,
#         messages=TextSendMessage(message))

#     return "access!"


#massage validation
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__" :
    app.run()