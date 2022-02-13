from django import forms


class SettingsForm(forms.Form):
    location = forms.CharField(max_length=100, required=False)

    location.widget.attrs.update(
        {'class': 'form-control',
         'disabled': 'True',
         'placeholder': 'Update your place of interest'}
    )
