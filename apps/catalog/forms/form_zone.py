# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models.model_zones import Zone
from apps.catalog.models.model_locations import Location


class ZoneForm(forms.ModelForm):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':''})) 
    #location=forms.ModelChoiceField(queryset = Location.objects.filter(client =_self.request.user.profile.client).all(),widget=forms.Select(attrs={'class':'form-control select2'})) 
    class Meta:
        model=Zone
        fields = ('id','name','location')
