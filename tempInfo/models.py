import datetime
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from server import settings

# Create your models here.
class TempInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='temp_info')

    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.temperature}°C at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    @property
    def is_older_than_a_week(self):
        return timezone.now() - self.timestamp > datetime.timedelta(weeks=1)

    class Meta:
        ordering = ['-timestamp']