from django import forms

class TextForm(forms.Form):
    text = forms.CharField(label="Text", max_length=280)

class CreateTextThroughTweetForm(forms.Form):
    text = forms.CharField(label="Text", max_length=280)
    ciphered_text = forms.CharField(label="Ciphered Text", max_length=280, required=False)