from django import forms
class FilesForm(forms.Form):
    image = forms.FileField(required=False)
