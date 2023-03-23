# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models.model_departments import Department


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':''})) 
    class Meta:
        model=Department
        fields = ('id','name',)
 
