# barriers/forms.py

from django import forms
from .models import MarketAccessBarrier

class BarrierCountryForm(forms.Form):
    countries_affected = forms.CharField(label='Country affected', max_length=100)

class ReportBarrierForm(forms.ModelForm):
    class Meta:
        model = MarketAccessBarrier
        fields = ['title', 'description']
