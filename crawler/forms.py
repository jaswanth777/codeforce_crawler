from django import forms

class HandleForm(forms.Form):
    handle=forms.CharField(label='Enter the Codeforces Handle',max_length=150)
