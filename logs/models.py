from django.db import models

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    event = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    message = models.JSONField()

    class Meta:
        db_table = 'logs'

    def __str__(self):
        return f"Log {self.id} - {self.recipient}"
