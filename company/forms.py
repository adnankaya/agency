from django import forms
from django.utils.translation import ugettext_lazy as _

from company.models import Contact

# internals


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = _('Full Name')
        self.fields['email'].label = _('Email')
        self.fields['message'].label = _('Message')
    class Meta:
        model = Contact
        fields = ('full_name', 'email', 'message')
