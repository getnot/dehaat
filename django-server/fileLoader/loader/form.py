from django import forms  
from django.core.validators import RegexValidator

class fileLoadingForm(forms.Form): 
    ''' from to get input data and file'''
    queryVariable  = forms.CharField(label="Query Variable",help_text="ex: To Pruchase", max_length = 20)  
    queryYear = forms.IntegerField(label="Query Year",help_text="ex: 2016")     
    file      = forms.FileField(label="Please Upload Balance Sheet") # for creating file input  