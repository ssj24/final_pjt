from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    score = forms.IntegerField(min_value=0, max_value=10)
    class Meta:
        model = Rating
        fields = ('score', 'comment',)
