# -*- coding: utf-8 -*-
from django import forms
from apps.acs.models.model_sensor import AcsSensor
from apps.main.models.model_datamfsb import DataMfsb

class AcsSensorForm(forms.ModelForm):
    critical_type_list = (
        ('max', 'Максимальный'),
        ('min', 'Минимальный'),
    )
    type_list = (
        (0, '< Не определен >'),
        (1, 'Датчик диоксида углерода (CO2)'),
        (2, 'Датчик оксида (CO)'),
        (3, 'Датчик метана (CH4)'),
    )

    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Наименование'})) 
    critical_value = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    type = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control select2','autofocus':''}), choices=type_list)
    ratio = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
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
    scale= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'','placeholder':'Шкала датчика'})) 
    norm_value_from = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    norm_value_to = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    danger_value_from = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    danger_value_to = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    critical_value_from = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 
    critical_value_to = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','type':'number','step':'0.1','autofocus':'',})) 

    class Meta:
        model=AcsSensor
        fields = ('id','zone','tag','name','critical_value',
                  'critical_type','value','active',
                  'unit','max_value','comments',
                  'ratio','scale','norm_value_from',
                  'norm_value_to','danger_value_from',
                  'danger_value_to','critical_value_from',
                  'critical_value_to','type',)


