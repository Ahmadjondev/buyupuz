import requests


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
            'Authorization': 'key=AAAA68-tYDU:APA91bHCh6GUXhemtrmVc5TfsCLJGdqeKgrbZSE4tfvx3plnWWiZUJrA-kraI0MwL2D-jAq-c5-pB4ASEZn6FihI2hwlDWhKQP5J8lphVNMUxWKqevimtsWpC7oNNqORQJW4pF2LE7AY',
            'Content-Type': 'application/json'
        }
        requests.post(fcm_url, headers=headers, json=notification_payload)
    except:
        print("Error")
