from django.db import models

class FitnessRecord(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    age = models.CharField(max_length=50)  # Predicted age group
    height = models.FloatField()  # Height in cm
    weight = models.FloatField()  # Weight in kg

    def __str__(self):
        return self.name
