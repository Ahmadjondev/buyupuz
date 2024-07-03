from django.forms import model_to_dict
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count
from order.models import Order
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDate

from order.serializers import OrderSerializer, OrderListSerializer
from tools.generate_token import check_token_manager
from tools.notifications import send_notification_v2


class SendNotification(APIView):
    def get(self, request):
        send_notification_v2(topic='admin', title='BuyUp', msg="FCM V2 Testing")
        return Response()


class OrderStatisticsView(APIView):
    def get(self, request):
        auth_token = self.request.headers['Authorization']
        admin_id = check_token_manager(auth_token)
        if admin_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        # manjs = model_to_dict(Manager.objects.get(id=admin_id))
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        game_id = request.query_params.get('game_id')
        user_id = request.query_params.get('user_id')
        order_status = request.query_params.get('status')
        today = timezone.now()
        # if not manjs['is_superadmin']:
            # user_id = admin_id
        current_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = (current_month_start + timezone.timedelta(days=32)).replace(day=1, microsecond=0)

        orders = Order.objects.filter(created_at__range=[current_month_start, current_month_end])

        if start_date and end_date:
            orders = Order.objects.filter(created_at__range=[parse_date(start_date), parse_date(end_date)])

        if game_id:
            orders = orders.filter(game__id=game_id)

        if user_id:
            orders = orders.filter(manager__id=user_id)

        if order_status is not None:
            orders = orders.filter(status=order_status)
        total_revenue = orders.aggregate(total_revenue=Sum('price'))['total_revenue']
        total_count = orders.count()
        average_order_value = orders.aggregate(avg_order_value=Avg('price'))['avg_order_value']
        total_orders = orders.aggregate(total_orders=Count('id'))['total_orders']

        revenue_by_game = orders.values('game__name').annotate(total_revenue=Sum('price')).order_by('-total_revenue')
        orders_count_by_date = orders.annotate(
            date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')).order_by('date')
        top_selling_games = orders.values('game__name').annotate(total_quantity=Count('id')).order_by('-total_quantity')

        # today orders income
        today_date_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        today_date_end = today.replace(hour=23, minute=59, second=59, microsecond=59)
        today_pay = orders.filter(created_at__range=(today_date_start, today_date_end))
        today_amount = today_pay.filter(status=1).aggregate(Sum('price'))['price__sum'] or 0
        today_waiting_amount = today_pay.filter(status=0).aggregate(Sum('price'))['price__sum'] or 0
        today_count = today_pay.count()
        waiting = orders.filter(status=0).count()
        success = orders.filter(status=1).count()
        reject = orders.filter(status=2).count()
        data = {
            'total': {
                'amount': total_revenue,
                'count': total_count,
            },
            'today': {
                'amount': today_amount,
                'waiting_amount': today_waiting_amount,
                'count': today_count,
            },
            'status': {
                'waiting': waiting,
                'success': success,
                'reject': reject,
            },
            'average_order_value': average_order_value,
            'total_orders': total_orders,
            'revenue_by_game': list(revenue_by_game),
            'orders_count_by_date': list(orders_count_by_date),
            'top_selling_games': list(top_selling_games),
        }

        return Response(data, status=status.HTTP_200_OK)
