import os
import requests
from flask import Flask, request, Response
import json

app = Flask(__name__)

address_api_itilium = os.environ['AddressApiItilium']
login_itilium = os.environ['LoginItilium']
password_itilium = os.environ['PasswordItilium']
auth_key = os.environ['AuthKey']


@app.route('/getWebhookInfo', methods=['GET'])
def getWebHookInfo():
    # это только на время теста, надо скрывать в продакшене
    ret = requests.post("https://api.telegram.org/bot" + auth_key + "/getWebhookInfo")
    return ret.text


@app.route('/setWebHook', methods=['GET'])
def setWebHook():
    dict_data = dict()
    address = request.url.replace("setWebHook", auth_key)
    print(address)
    dict_data.update({"url": address})

    print(dict_data)

    ret = requests.post("https://api.telegram.org/bot" + auth_key + "/setWebhook",
                        data=json.dumps(dict_data).encode('utf-8'),
                        headers={"Content-Type": "application/json"})

    return ret.text


@app.route('/removeWebHook', methods=['GET'])
def removeWebHook():
    dict_data = dict()
    dict_data.update({"url": ""})

    ret = requests.post("https://api.telegram.org/bot" + auth_key + "/setWebhook",
                        data=json.dumps(dict_data).encode('utf-8'),
                        headers={"Content-Type": "application/json"})

    return ret.text


@app.route('/' + auth_key, methods=['POST'])
def IncomingConnectionPost():
    print("new message")
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')

        update = json.loads(json_string)

        print("UnJSONed: " + str(update))
        print("update_id: " + str(update["update_id"]))
        content = ''
        try:
            request_itilium = requests.post(address_api_itilium, data=json_string,
                                            auth=(login_itilium, password_itilium))

            if request_itilium.status_code == 200 and request_itilium.ok:
                content = request_itilium.content

                if content != 'Действие не найдено!':
                    content = json.loads(content)
        except:
            print('Error getting data in Itilium')

        # message_data = {  # формируем информацию для отправки сообщения
        #     'chat_id': update['message']['chat']['id'],  # куда отправляем сообщение
        #     'text': "I'm <b>bot</b>",  # само сообщение для отправки
        #     'reply_to_message_id': update['message']['message_id'],
        #     # если параметр указан, то бот отправит сообщение в reply
        #     'parse_mode': 'HTML'  # про форматирование текста ниже
        # }
        #
        # try:
        #     requestTelegram = requests.post('https://api.telegram.org/bot' + auth_key + '/sendMessage', data=content)
        # except:
        #     print('Send message for user error')

    return Response(status=200)
