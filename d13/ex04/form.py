from django import forms

class TextForm(forms.Form):
    
    widget = forms.TextInput(attrs={'placeholder': 'Add value ?'})

    text = forms.CharField(widget=widget)