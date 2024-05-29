from django.forms import model_to_dict
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response

from user.models import CashbackOrder, Invite
from user.serializers import CashbackOrderSerializer, InviteSerializer


class CheckCashback(UpdateAPIView):
    serializer_class = CashbackOrderSerializer
    queryset = CashbackOrder

    def perform_update(self, serializer):
        cash_id = self.request.data['id']
        status_check = self.request.data['status']

        if status_check == 1:
            serializer.save(status=status_check)
        data = dict(serializer.validated_data)
        user_id = data['user']
        user_obj = Invite.objects.filter(user=user_id).first()
        user_json = model_to_dict(user_obj)
        if user_obj:
            cashback = float(user_json['cashback']) + float(data['amount'])
            invite_ser = InviteSerializer(user_obj, data={'cashback': cashback})
            if invite_ser.is_valid():
                invite_ser.save()
        return Response({'detail': "Bajarildi"})


class CashbackOrderView(ListAPIView):
    serializer_class = CashbackOrderSerializer
    queryset = CashbackOrder.objects.all().order_by('-id')
