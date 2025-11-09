from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()



class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()  # minutes
    calories = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout} ({self.date})"


class Diet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    meal = models.CharField(max_length=100)
    food_item = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.meal} ({self.calories} cal)"


class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight_kg} kg on {self.date}"
