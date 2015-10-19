from django import forms
from .models import SlotSet


class UploadFileForm(forms.Form):
    comment = forms.CharField(max_length=150)
    #file = forms.FileField(upload_to='mars/%Y%m%d/schedule-OLD1.xml')
    file = forms.FileField()

class SlotSetForm(forms.ModelForm):
    class Meta:
        model  = SlotSet
        fields = ['xmlfile', 'begin', 'end']
