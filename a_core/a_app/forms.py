from django import forms

class ChannelForm(forms.Form):
    title = forms.CharField(label="Title", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entre Channel Title'}))
    description = forms.CharField(label="Description", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entre Channel Description', 'rows': 7}))