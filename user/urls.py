from django.urls import path, include
from .views import Register, Login, PaymentView, GetUser, UpdateUserView, Logout, VerifyView, ResendCodeView, \
    InviteStatView, InviteCreateView, GoogleSign, CashbackOrdersView
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('register', Register.as_view()),
    path('verification', VerifyView.as_view()),
    path('resend-code', ResendCodeView.as_view()),
    path('login', Login.as_view()),
    path('google/sign', GoogleSign.as_view()),
    path('logout', Logout.as_view()),
    path('user', GetUser.as_view()),
    path('user/update', UpdateUserView.as_view()),
    path('payments', PaymentView.as_view()),
    path('payments/create', PaymentView.as_view()),
    path('invites', InviteStatView.as_view()),
    path('invites/create', InviteCreateView.as_view()),
    path('cashback', CashbackOrdersView.as_view()),  # create and list
]
