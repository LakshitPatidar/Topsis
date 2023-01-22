
from django.shortcuts import render
from .models import TopsisForm
from .topsis import topsis
import pandas as pd
from django.core.mail import EmailMessage
from django import forms

from django.core.mail import EmailMessage

def send_email_with_result(email, resultFileName):
    subject = 'TOPSIS Result'
    message = 'Please find the attached Topsis result file'
    email = EmailMessage(subject, message, to=[email])
    email.attach_file(resultFileName)
    email.send()



def topsis_view(request):
    if request.method == 'POST':
        form = TopsisForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.check_req()
                file_handle = request.FILES['input_file']
                df = pd.read_csv(file_handle)
                matrix=pd.DataFrame(df)
                weights = [float(x) for x in form.cleaned_data['weights'].split(',')]
                impacts = [str(x) for x in form.cleaned_data['impacts'].split(',')]
                if(len(weights)!=(len(matrix.columns)-1)):
                    raise forms.ValidationError("No of weights and impacts not equal to no of columns in dataset")
                result = topsis(weights, impacts,df)
                email = form.cleaned_data['email']
                result.to_csv("result.csv", index=False)
                send_email_with_result(email, "result.csv")
            except Exception as e:
                context = {'form': form, 'error_message': str(e)}
                return render(request, 'template.html', context)
    else:
        form = TopsisForm()
    context = {'form': form}
    return render(request, 'template.html', context)

