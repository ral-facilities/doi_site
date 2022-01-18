from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory, MultiWidget, TextInput
RT_CHOICES= [
    ('type 1', 'Type A'),
    ('type 2', 'Type B'),
    ('type 3', 'Type C'),
    ('type 4', 'Type D'),
    ]
class DoiForm(forms.Form):
    identifier = forms.CharField(label='Identifier', max_length=100)
    title = forms.CharField(max_length=100)
    publisher = forms.CharField(max_length=100)
    publication_year = forms.CharField(max_length=100)
    resource_type= forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES))
class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject')
SubjectFormset = formset_factory(SubjectForm, extra=1)
class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name')
    familyname = forms.CharField(label='Family Name')
    affiliation = forms.CharField(label='Affiliation')
   
CreatorFormset = formset_factory(CreatorForm, extra=1)





