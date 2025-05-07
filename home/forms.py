'''
Forms for the home app
History:
(forgot to add history until recently)
Feb 21 2024 - Finished ScrapCodeForm
'''

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from scrapbooks.models import Scrapbook

class ScrapCodeForm(forms.Form):
    '''
    Form to enter a scrapbook code (for the homepage)
    '''
    scrapcode = forms.CharField(label="Type in your unique code to add momentos to an existing scrapbook:", max_length=6)

    def clean_scrapcode(self):
        data = self.cleaned_data['scrapcode']

        # check if scrapbook code matches an existing scrapbook
        valid_codes = [s.scrapbook_code for s in Scrapbook.objects.all()] # codes of all scrapbooks
        if data not in valid_codes:
            raise ValidationError(_('Invalid code – this scrapbook does not exist'))

        return data