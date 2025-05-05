from django.db import models

# Create your models here.

class Finance(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    transaction_Description = models.TextField()
    category = models.CharField(max_length=255)
    amount = models.FloatField()
    type = models.CharField(max_length=255)
    user_id = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.date} | {self.type}: ${self.amount}"

    class Meta:
        db_table = "finance"

class ChatMessage(models.Model):
    message = models.TextField()
    sender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message}"
    