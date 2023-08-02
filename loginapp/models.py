from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserLoginHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_duration = models.IntegerField(default=0)
    last_logout_time = models.DateTimeField(null=True, blank=True)

    def update_duration(self, duration):
        self.total_duration += duration
        self.last_logout_time = timezone.now()
        self.save()

