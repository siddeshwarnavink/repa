from django import forms
from .models import Process, ProcessFile

class ProcessForm(forms.ModelForm):
    preferred_education = forms.MultipleChoiceField(
        choices=[
            ('B.Tech', 'B.Tech'),
            ('M.Tech', 'M.Tech'),
            ('MCA', 'MCA'),
            ('BCA', 'BCA'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Process
        fields = ['job_title', 'required_skills', 'min_experience_years', 'must_have_keywords', 'preferred_education']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g: Senior Machine Learning Engineer'}),
            'min_experience_years': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g: 2'})
        }

class ProcessFileForm(forms.ModelForm):
    class Meta:
        model = ProcessFile
        fields = ['file']
