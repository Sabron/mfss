# -*- coding: utf-8 -*-
from django import forms
from apps.scada.models.model_sensor import ScadaSensor

class ScadaSensorForm(forms.ModelForm):
    tag = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','readonly':'','placeholder':'ТЭГ'})) 
    position = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Позиция'})) 
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Наименование'})) 
    active=forms.BooleanField(widget=forms.CheckboxInput(),required = False)

    class Meta:
        model=ScadaSensor
        fields = ('id','zone','tag','position','name','value','active',)



