from django.urls import path

from .apis.apps_buyup import CarouselCreateView, RedeemCreateView, NotificationCreateView, RedeemListView, \
    CarouselDeleteView
from .apis.cashback import CheckCashback
from .apis.games import GameUpdateView, CreateGameView, GameDeleteView, GamesAdminView
from .apis.items import CreateItemView, ItemDeleteView, ItemUpdateView, ListItemView
from .apis.statics import OrderStatisticsView, SendNotification
from .apis.users import GiveWarningView, UserListView
from .views import CheckOrderView, CheckPaymentView, PaymentListView, OrderListView, Login, UsersBalance, GetAdmin, \
    Statics
from .apis.rest_time import RestTimeAdminView

urlpatterns = [
    # views.py
    path('login', Login.as_view()),
    path('manager', GetAdmin.as_view()),
    path('payments', PaymentListView.as_view()),
    path('orders', OrderListView.as_view()),
    path('orders/check', CheckOrderView.as_view()),
    path('payments/check', CheckPaymentView.as_view()),
    path('rest-time', RestTimeAdminView.as_view()),
    path('statics', Statics.as_view()),
    path('cashback', Statics.as_view()),
    path('cashback/check', CheckCashback.as_view()),

    # users.py
    path('users/spam', GiveWarningView.as_view()),
    path('users', UserListView.as_view()),

    # games.py
    path('games', GamesAdminView.as_view()),
    path('games/create', CreateGameView.as_view()),
    path('games/update/<int:pk>', GameUpdateView.as_view()),
    path('games/delete/<int:pk>', GameDeleteView.as_view()),

    # items.py
    path('items', ListItemView.as_view()),
    path('items/create', CreateItemView.as_view()),
    path('items/delete/<int:pk>', ItemDeleteView.as_view()),
    path('items/update/<int:pk>', ItemUpdateView.as_view()),

    # apps_buyup.py "PATCH /admin/v2/items/update/1 HTTP/1.1"
    path('carousels/create', CarouselCreateView.as_view()),
    path('notifications/create', NotificationCreateView.as_view()),
    path('redeems/create', RedeemCreateView.as_view()),
    path('redeems', RedeemListView.as_view()),
    path('carousels/delete/<int:pk>', CarouselDeleteView.as_view()),

    path('users/balance', UsersBalance.as_view()),

    path('order/statics', OrderStatisticsView.as_view()),
    path('notif', SendNotification.as_view())
]
