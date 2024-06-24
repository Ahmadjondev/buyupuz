from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentCreateSerializer
from tools.generate_token import checkToken
from tools.secure import checkAPI


class PaymentView(ListAPIView):
    serializer_class = PaymentSerializer

    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        payments = Payment.objects.filter(user_id=user_id).order_by('-id')

        return payments

    def post(self, request):
        token = request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        datas = {'price': self.request.data['price'],
                 'screenshot': self.request.data['screenshot'],
                 'user': user_id}
        serializer = PaymentCreateSerializer(data=datas)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            send_notification_v2("admin", f"To`lov qilindi",
                                 f"Foydalanuvchi to`lov qildi va hozir siz tasdiqlashingiz kerak")
        except:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)
