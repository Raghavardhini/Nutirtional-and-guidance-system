from django import forms

class FitnessForm(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.ImageField()
    height = forms.FloatField()  # Height in cm
    weight = forms.FloatField()  # Weight in kg
