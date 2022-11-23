# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models.model_locations import Location


class LocationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':''})) 
    class Meta:
        model=Location
        fields = ('id','name',)
 