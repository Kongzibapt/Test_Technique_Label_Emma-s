from django import forms

class DatesForm(forms.Form):
    start_date = forms.DateField(label="Start date",input_formats=['%d/%m/%Y'], required=True)
    end_date = forms.DateField(label="End date",input_formats=['%d/%m/%Y'], required=True,)
