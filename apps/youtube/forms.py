from django import forms
from .models import Song


class SongForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update({'class': 'form-control mb-4',
                                                'placeholder': 'Paste URL of the song here ...',
                                                'type': 'search',
                                                })
        self.fields['title'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Give a name to your song, e.g. ABBA - Waterloo ...',
                                                  'type': 'text',
                                                  })

    class Meta:
        model = Song
        exclude = ['downloaded']
        fields = ['url', 'title']
