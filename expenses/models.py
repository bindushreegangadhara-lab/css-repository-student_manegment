from django.db import models

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.FloatField()
    category = models.CharField(max_length=100, default="General")  # ✅ ADD DEFAULT
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
