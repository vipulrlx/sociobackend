from django.db import models
from .business import Business

class Product(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='products'
    )
    product_name = models.CharField(max_length=255)
    product_info = models.TextField()
    product_usp = models.TextField()
    target_region = models.CharField(max_length=255)
    existing_gtm = models.TextField()
    team_size = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name