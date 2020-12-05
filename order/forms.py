from django import forms

from . import models


_MDL_ATTRS = {'class': 'mdl-textfield__input'}


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('contractor', 'total', 'text')
        widgets = {
            'contractor': forms.TextInput(attrs=_MDL_ATTRS),
            'total': forms.NumberInput(attrs={'min': 0, **_MDL_ATTRS}),
            'text': forms.Textarea(attrs=_MDL_ATTRS),
        }
