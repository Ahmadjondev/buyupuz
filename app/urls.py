from django.urls import path
from .views import (
    CarouselListView, NotificationListView, RedeemCheckView, RestTimeView, PaymentCardView,
)

urlpatterns = [
    path('carousels', CarouselListView.as_view()),
    path('redeems/check', RedeemCheckView.as_view()),
    path('notifications', NotificationListView.as_view()),
    path('rest-time', RestTimeView.as_view()),
    path('cards', PaymentCardView.as_view()),
]
