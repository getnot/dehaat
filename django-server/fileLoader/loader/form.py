from django import forms  
from django.core.validators import RegexValidator

class fileLoadingForm(forms.Form): 
    ''' from to get input data and file'''
    queryVariable  = forms.CharField(label="Query Variable",help_text="Please Enter Query Variable", max_length = 20)  
    queryYear = forms.IntegerField(label="Query Year",help_text="Please Enter The relevant year")     
    file      = forms.FileField(label="Please Upload Balance Sheet") # for creating file input  