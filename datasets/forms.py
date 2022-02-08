from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory, MultiWidget, TextInput
RT_CHOICES= [
    ('Audiovisual', 'Audiovisual'),
    ('Book', 'Book'),
    ('BookChapter', 'BookChapter'),
    ('Collection', 'Collection'),
    ('ComputationalNotebook', 'ComputationalNotebook'),
    ('ConferencePaper', 'ConferencePaper'),
    ('ConferenceProceeding', 'ConferenceProceeding'),
    ('DataPaper', 'DataPaper'),
    ('Dataset', 'Dataset'),
    ('Dissertation', 'Dissertation'),
    ('Event', 'Event'),
    ('Image', 'Image'),
    ('InteractiveResource', 'InteractiveResource'),
    ('Journal', 'Journal'),
    ('JournalArticle', 'JournalArticle'),
    ('Model', 'Model'),
    ('OutputManagementPlan', 'OutputManagementPlan'),
    ('PeerReview', 'PeerReview'),
    ('PhysicalObject', 'PhysicalObject'),
    ('Preprint', 'Preprint'),
    ('Report', 'Report'),
    ('Service', 'Service'),
    ('Software', 'Software'),
    ('Sound', 'Sound'),
    ('Standard', 'Standard'),
    ('Text', 'Text'),
    ('Workflow', 'Workflow'),
    ('Other', 'Other')
    ]

class DoiForm(forms.Form):
    identifier = forms.CharField(label='Identifier', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Identifier', 'class':' form-control form-control-sm'}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':' form-control form-control-sm'}))
    publisher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Publisher', 'class':' form-control form-control-sm'}))
    publication_year = forms.IntegerField(label='Pick the year:', min_value=1975, max_value=2100, widget=forms.NumberInput(attrs={'placeholder': 'Publication Year', 'class':' form-control form-control-sm'}))

    resource_type= forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES, attrs={'class':' form-select form-select-sm'}))
class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject', required=False, widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class':' form-control form-control-sm'}))
SubjectFormset = formset_factory(SubjectForm, extra=1)
class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name', widget=forms.TextInput(attrs={'placeholder': 'Given Name', 'class':' form-control form-control-sm'}))
    familyname = forms.CharField(label='Family Name', widget=forms.TextInput(attrs={'placeholder': 'Family Name', 'class':' form-control form-control-sm'}))
    affiliation = forms.CharField(label='Affiliation',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Affiliation', 'class':' form-control form-control-sm'}))
   
CreatorFormset = formset_factory(CreatorForm, extra=0,  min_num=1, validate_min=True)

class UrlForm(forms.Form):
    url = forms.CharField(label='Url', widget=forms.TextInput(attrs={'class':' form-control form-control-sm'}))




