from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tools.notifications import sendNotification
from user.models import User
from user.serializers import UserUpdateSerializer


class UserListView(ListAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class GiveWarningView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['id'])
            json_user = dict(UserUpdateSerializer(user).data)
            json_user['spam'] += 1
            update_user = UserUpdateSerializer(user, json_user)
            update_user.is_valid(raise_exception=True)
            update_user.save()
            if int(json_user['spam']) > 2:
                sendNotification(json_user['notification_token'], 'Ogohlantirish!',
                                 "Admin sizni blokladi")
            else:
                sendNotification(json_user['notification_token'], 'SPAM',
                                 "Admin sizga ogohlantirish berdi")
            return Response({}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
