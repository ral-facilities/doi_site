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
    identifier = forms.CharField(label='Identifier', max_length=100)
    title = forms.CharField(max_length=100)
    publisher = forms.CharField(max_length=100)
    publication_year = forms.CharField(max_length=100)
    resource_type= forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES))
class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject', required=False)
SubjectFormset = formset_factory(SubjectForm, extra=1)
class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name')
    familyname = forms.CharField(label='Family Name')
    affiliation = forms.CharField(label='Affiliation')
   
CreatorFormset = formset_factory(CreatorForm, extra=1)

class UrlForm(forms.Form):
    url = forms.CharField(label='Url')




