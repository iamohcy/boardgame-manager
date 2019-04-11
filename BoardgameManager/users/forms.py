from django import forms


class LinkBggForm(forms.Form):
    bgg_username = forms.CharField(min_length=4, max_length = 20, label="",
                                   widget=forms.TextInput(attrs={'placeholder': 'BGG Username'}))

