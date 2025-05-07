'''
Forms for the scrapbooks app
History:
Feb 23 2024 - File creation
Feb 29 2024 - created UploadContentForm
Mar 04 2024 - tried to hide scrapbook field on UploadContentForm and did not succeed
Mar 19 2024 - added InfoForm
Mar 21 2024 - fixed THEME_CHOICES so the dropdown works
Mar 25 2024 - changed UploadContentForm parent class back to ModelForm and finally got rid of 'scrapbook' field
Mar 27 2024 - changed InfoForm parent class to ModelForm
Apr 01 2024 - added widgets dictionary to InfoForm for bootstrap CSS
Apr 12 2024 - UploadContentForm() is now a ModelForm, not regular Form; added EditCaptionForm
Apr 18 2024 - included changes to UploadContentForm
'''

from django.forms import ModelForm
from django import forms
from .models import Media, Scrapbook

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UploadContentForm(ModelForm):
    '''
    Form to input caption and image for a new Media object
    '''
    class Meta:
        model = Media
        fields = ["caption", "image"]
        widgets = {
            'caption' : forms.TextInput(attrs={'class': ' form-control font-monospace m-2 bg-warning'}),
            'image' : forms.ClearableFileInput(attrs={'class': 'form-control font-monospace m-2 bg-warning'})
        }


class InfoForm(ModelForm):
    '''
    form to enter information about a scrapbook project
    '''
    class Meta:
        model = Scrapbook
        fields = ["scrapbook_name", "scrapbook_theme"]
        widgets = {
            'scrapbook_name': forms.TextInput(attrs={'class': 'form-control font-monospace bg-warning mt-2'}),
            'scrapbook_theme': forms.Select(attrs={'class': 'form-select font-monospace bg-warning mt-2'})
        }

class EditCaptionForm(ModelForm):
    '''
    Just for editing the caption of a Media object
    '''
    class Meta:
        model = Media
        fields = ["caption"]