from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Activity(models.Model):
    title=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True, blank=True)
    user=models.CharField(max_length=200)
    options=(
        ("pending","pending"),
        ("completed","completed"),
        ("in-progress","in-progress")
    )
    status=models.CharField(max_length=200, choices=options, default="pending")
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) :
        return self.title