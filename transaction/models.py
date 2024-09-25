from django.db import models

class Transaction(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount) + "원"