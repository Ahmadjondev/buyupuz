import os

from django.db.models import Sum
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response

from app.models import Carousel, Redeem, Notification
from app.serializers import CarouselSerializer, RedeemSerializer, NotificationSerializer, RedeemListSerializer
from tools.notifications import sendNotification


class CarouselCreateView(CreateAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer


class NotificationCreateView(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        try:
            data = serializer.data
            sendNotification('/topics/admin', data['title'], data['description'], data=data)
            print(serializer.data)
        except:
            pass


class RedeemCreateView(CreateAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer


# All Redeem
class RedeemListView(ListAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer
    # serializer_class = RedeemListSerializer

    # def list(self, request, *args, **kwargs):
    #     query = self.get_queryset()
    #     redeem = Redeem.objects.filter(status=True)
    #     used = redeem.aggregate(Sum('price'))['price__sum'] or 0
    #     serializer = self.get_serializer(query, many=True)
    #     return Response({
    #         "used": used,
    #         "redeems": serializer.data
    #     })


class CarouselDeleteView(DestroyAPIView):
    serializer_class = CarouselSerializer
    queryset = Carousel.objects.all()

    def perform_destroy(self, instance):
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
        instance.delete()
