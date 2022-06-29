from django.db import models

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    seller_id = models.ForeignKey("users.User",on_delete=models.CASCADE,related_name="products")