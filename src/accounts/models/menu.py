from django.db import models
from django.utils import timezone

class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web'),
        ('mobile', 'Mobile'),
    ]
    
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    sequence = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., fas fa-home)")
    destination_url = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='web')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['sequence']

    def __str__(self):
        return self.display_name

class SubMenu(models.Model):
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='submenus')
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    sequence = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., fas fa-user)")
    destination_url = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'submenu'
        verbose_name = 'Sub Menu'
        verbose_name_plural = 'Sub Menus'
        ordering = ['parent_menu', 'sequence']

    def __str__(self):
        return f"{self.parent_menu.display_name} - {self.display_name}" 