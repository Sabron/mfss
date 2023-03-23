# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models.model_workers import Worker
from apps.catalog.models.model_positions import Position
from apps.catalog.models.model_departments import Department



class WorkerForm(forms.ModelForm):
    CHOICES = (
        ('m', 'Мужской'),
        ('f', 'Женский'),
    )

    tabnomer = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class':'form-control','autofocus':''})) 
    lastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Фамилия','class':'form-control','autofocus':''}))
    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя','class':'form-control'}))
    otchestvo = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder':'Отчество','class':'form-control'}))
    sex_workers = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control select2','autofocus':''}), choices=CHOICES)
    department = forms.ModelChoiceField(queryset = Department.objects.all(),widget=forms.Select(attrs={'class':'form-control select2'}))
    position = forms.ModelChoiceField(queryset = Position.objects.all(),widget=forms.Select(attrs={'class':'form-control select2'}))

    class Meta:
        model=Worker
        fields = ('id','tabnomer','lastName','firstName','lastName','otchestvo','sex_workers','department','position')
    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)
