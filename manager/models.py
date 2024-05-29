from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)
    password = models.CharField(max_length=255, blank=True, null=True)
    notification_token = models.CharField(max_length=1001, null=True, blank=True)
    role = models.SmallIntegerField(default=0)
    sign_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # games = models.ForeignKey(Game, blank=True, null=True)

    def __str__(self):
        return self.name