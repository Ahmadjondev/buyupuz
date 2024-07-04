from django.db.models import Sum
from datetime import datetime, timedelta

from game.models import Game, Order
from user.models import User
import requests

def format_currency(amount):
    integer_part, fractional_part = str(amount).split('.')
    integer_part_formatted = ' '.join(integer_part[::-1][i:i + 3] for i in range(0, len(integer_part), 3))[::-1]

    formatted_amount = f"{integer_part_formatted}.{fractional_part}"

    return formatted_amount


def send_statics(): 
    bot_token = "6769633037:AAEHXLIzsEVrTVxPfJKhYmzYvWz6x1_mbOI"
    chat_id = "-1002039386599"

    try:
        time = datetime.now()
        formatted_date = time.strftime("%d.%m.%Y %H:%M UTC%z")
        users = User.objects.all()
        users_count = users.count()
        today_date_start = time.replace(hour=0, minute=0, second=1, microsecond=0)
        today_date_end = time.replace(hour=23, minute=59, second=59, microsecond=59)
        current_month_start = time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1, microsecond=0)

        today_users_count = users.filter(created_at__range=(today_date_start, today_date_end)).count()
        orders = Order.objects.all()
        orders_count = orders.count()
        orders_month = orders.filter(status=1, created_at__range=(current_month_start, current_month_end))
        orders_month_count = orders_month.count()
        orders_today = orders_month.filter(created_at__range=(today_date_start, today_date_end))
        orders_today_count = orders_today.count()
        orders_today_amount = orders_today.aggregate(Sum('price'))['price__sum'] or 0

        text = f'''Bugungi statistika 

📅 Sana: {formatted_date}

👤 Jami foydalanuvchilar soni:   {users_count} ta
👤 Bugun qo'shilgan foydalanuvchilar soni:  {today_users_count} ta

📦 Jami buyurtmalar soni: {orders_count} ta 
📦 Bu oydagi buyurtmalar soni:   {orders_month_count} ta
📦 Bugungi buyurtmalar soni: {orders_today_count} ta
💵 Bugungi pul aylanmasi: {format_currency(orders_today_amount)} so'm'''

        # send message to admin group
        api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        response = requests.post(
            api_url,
            data={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown',
            },
        )
        result = response.json()
        pin_url = f'https://api.telegram.org/bot{bot_token}/pinChatMessage'
        requests.post(
            pin_url,
            data={
                'chat_id': chat_id,
                'message_id': result['result']['message_id'],
            },
        )
    except:
        # send message to admin group
        api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        respon = requests.post(
            api_url,
            data={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown',
            },
        )
        respons = requests.post(
            api_url,
            data={
                'chat_id': chat_id,
                'text': "BUGGGG",
                'parse_mode': 'Markdown',
            },
        )

def send_games_statics():
    bot_token = "6769633037:AAEHXLIzsEVrTVxPfJKhYmzYvWz6x1_mbOI"
    chat_id = "-1002039386599"
    # time = datetime.now()

    # today_date_start = time.replace(hour=0, minute=0, second=1, microsecond=0)
    # today_date_end = time.replace(hour=23, minute=59, second=59, microsecond=59)
    # games = Game.objects.filter(visible=True).values()
    # orders = Order.objects.filter(status=1, created_at__range=(today_date_start, today_date_end))

    # statics_for_games = ""

    # for game in games:
    #     orders_for_game = orders.filter(game=int(game['id']))
    #     orders_amount = orders_for_game.filter(game=int(game['id'])).aggregate(Sum('price'))['price__sum'] or 0
    #     statics_for_games += f"{game['name']}\nBuyurtma soni: {orders_for_game.count()}\nBuyurtmalar narxi: {format_currency(orders_amount)}\n-----------------"

    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    requests.post(
            api_url,
            data={
                'chat_id': chat_id,
                'text': 'statics_for_games',
                'parse_mode': 'Markdown',
            },
        )    

