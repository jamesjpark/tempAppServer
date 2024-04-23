from decimal import Decimal
from rest_framework import status, views
from rest_framework.response import Response
from .models import TempInfo
from .serializers import TempInfoSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TempInfoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = TempInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        now = timezone.now()
        start_time = now - timedelta(hours=1)
        try:
            records = TempInfo.objects.filter(user=request.user, timestamp__gte=start_time)
        except TempInfo.DoesNotExist:
            return Response({"message": "No records found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TempInfoSerializer(records, many=True)
        return Response(serializer.data)


class AverageTemperatureView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, period):
        """
        Calculate the average temperature for a specified time period.
        Period can be 'hour', 'day', or 'week'.
        """
        now = timezone.now()
        time_deltas = {
            'hour': timedelta(hours=1),
            'day': timedelta(days=1),
            'week': timedelta(weeks=1)
        }
        if period in time_deltas:
            start_time = now - time_deltas[period]
            average_temp = TempInfo.objects.filter(
                user=request.user,
                timestamp__gte=start_time
            ).aggregate(Avg('temperature'))

            average_temperature = average_temp['temperature__avg']
            if average_temperature is not None:
                return Response({'status': 'success', 'average_temperature': round(average_temperature, 2)})
            else:
                return Response({'status': 'error', 'message': 'No temperature data available for the specified period'}, status=404)
        else:
            return Response({'status': 'error', 'message': 'Invalid period specified'}, status=400)