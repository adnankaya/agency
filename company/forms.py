from django import forms
from django.utils.translation import ugettext_lazy as _

from company.models import ContactMessage

# internals


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = _('Full Name')
        self.fields['full_name'].css_class = 'form-control' 
        self.fields['email'].label = _('Email')
        self.fields['message'].label = _('Message')
    class Meta:
        model = ContactMessage
        fields = ('full_name', 'email', 'message')
