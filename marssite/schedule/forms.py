from django import forms
from django.contrib.postgres.forms import DateRangeField

from .models import SlotSet, Proposal
from natica.models import Telescope,Instrument


class UploadFileForm(forms.Form):
    comment = forms.CharField(max_length=150)
    #file = forms.FileField(upload_to='mars/%Y%m%d/schedule-OLD1.xml')
    file = forms.FileField()

class SlotSetForm(forms.ModelForm):
    class Meta:
        model  = SlotSet
        fields = ['xmlfile', 'comment']

class BatchSlotSetForm(forms.Form):
    telescope = forms.ModelChoiceField(queryset=Telescope.objects.all(),
                                        help_text='Pick one')
    #!instrument = forms.ModelChoiceField(queryset=Instrument.objects.none())
    instrument = forms.ModelChoiceField(queryset=Instrument.objects.all(),
                                        help_text='Pick one')
    prop = forms.ModelChoiceField(queryset=Proposal.objects.all(),
                                        help_text='Pick one')
    split = forms.BooleanField(
        initial=True, required=False,
        help_text='Iff TRUE treat a slot as Split Night')

    start_date = forms.DateField(help_text='YYYY-MM-DD')
    end_date = forms.DateField(help_text='YYYY-MM-DD')


#!    def __init__(self):
#!        super(BatchSlotSetForm, self).__init__()
#!        self.fields['instrument'].querset = Instrument.objects.all()
        
