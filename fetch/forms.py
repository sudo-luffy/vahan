from django import forms

class CSVUploadForm(forms.Form):
    email = forms.EmailField(label='Your Email', required=True)
    csv_file = forms.FileField(label='Upload CSV', required=True)
