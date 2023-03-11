from django import forms
from .models import Details,Leave


class info(forms.ModelForm):
    class Meta:
        model=Details
        fields="__all__"

class leaveinfo(forms.ModelForm):
    class Meta:
        model=Leave
        fields="__all__"