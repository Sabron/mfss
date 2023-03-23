# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models.model_positions import Position


class PositionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':''})) 
    class Meta:
        model=Position
        fields = ('id','name',)
 

