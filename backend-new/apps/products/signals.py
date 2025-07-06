"""
Signals for products app.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, ProductSale


@receiver(post_save, sender=Product)
def update_category_product_count(sender, instance, **kwargs):
    """
    Update category product count when product is saved.
    """
    if instance.category:
        instance.category.update_product_count()


@receiver(post_delete, sender=Product)
def update_category_product_count_on_delete(sender, instance, **kwargs):
    """
    Update category product count when product is deleted.
    """
    if instance.category:
        instance.category.update_product_count()


@receiver(post_save, sender=ProductSale)
def update_seller_stats(sender, instance, created, **kwargs):
    """
    Update seller statistics when a sale is made.
    """
    if created:
        profile = instance.seller.profile
        profile.total_sales += 1
        profile.save()