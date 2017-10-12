# backend/forms.py

from django import forms
from mptt.forms import TreeNodeChoiceField
from barriers.models import BarrierRecord, BarrierType

class ChooseBarrierTypeForm(forms.Form):
    barrier_type = TreeNodeChoiceField(
        queryset=BarrierType.objects.filter(barrier_source=1),
    )

    def __init__(self, *args, **kwargs):
        super(ChooseBarrierTypeForm, self).__init__(*args, **kwargs)
        self.fields['barrier_type'].widget.attrs.update({'class' : 'c-form-control'})
