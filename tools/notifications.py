import json

import requests
import google.auth.transport.requests

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def sendNotification(token, title, msg, data=None,is_admin=None):
    try:
        if is_admin:
            bot_token = "7044795068:AAEv-d3QXACY_qnr_PAqagOnKgSpHdIfep4"
            chat_id = "6664784902"
            api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            requests.post(
                api_url,
                data={
                    'chat_id': chat_id,
                    'text': f"{title}\n{msg}",
                    'parse_mode': 'Markdown',
                },
            )
    except:
        pass
    try:
        notification_payload = {
            "to": token,
            "notification": {
                "title": title,
                "body": msg
            },
            "data": data
        }
        fcm_url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            'Authorization': 'key=AAAA68-tYDU:APA91bHCh6GUXhemtrmVc5TfsCLJGdqeKgrbZSE4tfvx3plnWWiZUJrA-kraI0MwL2D-jAq'
                             '-c5-pB4ASEZn6FihI2hwlDWhKQP5J8lphVNMUxWKqevimtsWpC7oNNqORQJW4pF2LE7AY',
            'Content-Type': 'application/json'
        }
        requests.post(fcm_url, headers=headers, json=notification_payload)
    except:
        print("Error")


def send_notification_v2(title, msg, token=None, topic=None, data=None, is_order_or_payment=False):
    if is_order_or_payment or topic:
        try:
            bot_token = "7044795068:AAEv-d3QXACY_qnr_PAqagOnKgSpHdIfep4"
            chat_id = "6664784902"
            api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            requests.post(
                api_url,
                data={
                    'chat_id': chat_id,
                    'text': f"{title}\n{msg}",
                    'parse_mode': 'Markdown',
                },
            )
        except:
            pass

    fcm_message = {}
    if topic:
        fcm_message = {
            "message": {
                "topic": topic,
                "notification": {
                    "title": title,
                    "body": msg
                },
                "data": data
            }
        }
    else:
        fcm_message = {
            "message": {
                "token": token,
                "notification": {
                    "title": title,
                    "body": msg
                },
                "data": data
            }
        }
    FCM_URL = "https://fcm.googleapis.com/v1/projects/buyupuz/messages:send"
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
    }

    resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)
    # return resp.text
    if resp.status_code == 200:
        print('Message sent to Firebase for delivery, response:')
        print(resp.text)
    else:
        print(resp.text)
        print("--------------------")
        print(resp.content)


def _get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        'config/firebase-admin.json', scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    print(credentials.token)
    return credentials.token
