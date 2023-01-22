from django import forms
import pandas as pd

class TopsisForm(forms.Form):
    input_file = forms.FileField()
    weights = forms.CharField(max_length=255)
    impacts = forms.CharField(max_length=255)
    email = forms.EmailField()

    def check_req(self):
        weights = self.cleaned_data.get('weights')
        impacts = self.cleaned_data.get('impacts')
        if weights:
            comma=0
            for i in range(0,len(weights)):
                if(weights[i]==','):
                    comma=comma+1
            if(comma==0):
                raise forms.ValidationError("Pls enter weights seperated by commas")
            try:    
                weights = [str(x) for x in weights.split(',')]
            except:
                raise forms.ValidationError("Pls enter numeric values")
        else:
            raise forms.ValidationError("Weights field is required.")
        if impacts:
            comma=0
            for i in range(0,len(impacts)):
                if(impacts[i]==','):
                    comma=comma+1
            if(comma==0):
                raise forms.ValidationError("Pls enter impacts seperated by commas")
            impacts = [str(x) for x in impacts.split(',')]
            for i in range(0,len(impacts)):
                if not(impacts[i]=='+' or impacts[i]=='-'):
                    raise forms.ValidationError("Impacts should be either + or -")
        else:
            raise forms.ValidationError("Impacts field is required.")
        if len(weights) != len(impacts):
            raise forms.ValidationError("Number of weights must be equal to number of impacts")
    
