# -*- coding: utf-8 -*-
from django import forms
from apps.acs.models.model_sensor import AcsSensor
from apps.main.models.model_datamfsb import DataMfsb

class AcsSensorForm(forms.ModelForm):
    critical_type_list = (
        ('max', 'Максимальный'),
        ('min', 'Минимальный'),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Наименование'})) 
    critical_value = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    step = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.01','autofocus':'',})) 
    ratio = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'any','autofocus':'',})) 
    max_value = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    critical_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class':'form-control select2',
                'autofocus':''}),
        choices=critical_type_list)
    #value = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.00001','autofocus':'',})) 
    active=forms.BooleanField(widget=forms.CheckboxInput(),required = False)
    unit= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Единица измерения'})) 
    comments = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control','autofocus':'','placeholder':'Комментарий'})) 
    class Meta:
        model=AcsSensor
        fields = ('id','tag','name','critical_value','critical_type','value','active','unit','max_value','comments','ratio','step')


