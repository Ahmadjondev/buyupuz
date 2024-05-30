from django.urls import path

from payment.views import PaymentView

urlpatterns = [
    path('payments', PaymentView.as_view()),
    path('payments/create', PaymentView.as_view()),
]
