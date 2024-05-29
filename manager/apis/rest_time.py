from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Working
from app.serializers import RestTimeSerializer


class RestTimeAdminView(APIView):
    def get(self, request):
        try:
            first = Working.objects.all().first()
            json = RestTimeSerializer(first).data
            current_time = datetime.now()
            current_str = f"{f'0{current_time.hour}' if current_time.hour < 10 else current_time.hour}:{f'0{current_time.minute}' if current_time.minute < 10 else current_time.minute}"
            status_time = True
            if ((current_str >= json['start_time'] or current_str <= json['end_time'])
                    and json['start_time'] > json['end_time']):
                status_time = False
            response_json = {
                'start': json['start_time'],
                'end': json['end_time'],
                'working': status_time,
                'status': json['status'],
                'comment': json['comment']
            }
            return Response(response_json)
        except:
            return Response({'detail': "Vaqt mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # try:
        start = request.data['start']
        end = request.data['end']
        status_work = request.data['status']
        comment = request.data['comment']

        first = Working.objects.all().first()
        if first:
            rest = RestTimeSerializer(first, data={
                'start_time': start,
                'end_time': end,
                'status': status_work,
                'comment': comment
            })
            rest.is_valid(raise_exception=True)
            rest.save()
        else:
            Working.objects.create(start_time=start, end_time=end, status=status_work)
        return Response({}, status=status.HTTP_200_OK)
