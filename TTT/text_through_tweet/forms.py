from django import forms

class TextForm(forms.Form):
    text = forms.CharField(label="Text", max_length=280)