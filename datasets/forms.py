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

YR_CHOICES=[]
for x in range (1975, 2100, 1):
    YR_CHOICES.append(x)
class DoiForm(forms.Form):
    identifier = forms.CharField(label='Identifier', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Identifier'}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    publisher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Publisher'}))
    # publication_year = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'Publication Year'}))
    publication_year = forms.CharField(label='Pick the year:', widget=forms.SelectDateWidget(years=YR_CHOICES))

    resource_type= forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES))
class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject', required=False, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
SubjectFormset = formset_factory(SubjectForm, extra=1)
class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name', widget=forms.TextInput(attrs={'placeholder': 'Given Name'}))
    familyname = forms.CharField(label='Family Name', widget=forms.TextInput(attrs={'placeholder': 'Family Name'}))
    affiliation = forms.CharField(label='Affiliation',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Affiliation'}))
   
CreatorFormset = formset_factory(CreatorForm, extra=0,  min_num=1, validate_min=True)

class UrlForm(forms.Form):
    url = forms.CharField(label='Url')




