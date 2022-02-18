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
    identifier = forms.CharField(label='Identifier', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Identifier', 'class':'form-control form-control-sm', 'id':'identifier'}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'form-control form-control-sm', 'id':'title'}))
    publisher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Publisher', 'class':'form-control form-control-sm', 'id':'publisher'}))
    publication_year = forms.IntegerField(label='Pick the year:', min_value=1975, max_value=2100, widget=forms.NumberInput(attrs={'placeholder': 'Publication Year', 'class':'form-control form-control-sm', 'id':'publicationYear'}))
    resource_type = forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES, attrs={'class':'form-select form-select-sm', 'id':'resourceType'}))
    resource_type_text = forms.CharField(label='Resource type:', required=False, widget=forms.TextInput(attrs={'placeholder': 'Resource type', 'class':'form-control form-control-sm', 'id':'resourceType'}))
    abstract = forms.CharField(label='Abstract', required=False, widget=forms.Textarea(attrs={'placeholder': 'Abstract',"rows":3, 'class':'form-control form-control-sm', 'id':'abstract'}))
    version = forms.CharField(label='Version', required=False, widget=forms.TextInput(attrs={'placeholder': 'Version', 'class':'form-control form-control-sm', 'id':'version'}))

class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject', required=False, widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class':'form-control form-control-sm', 'id':'subject'}))
SubjectFormset = formset_factory(SubjectForm, extra=1)

class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name', widget=forms.TextInput(attrs={'placeholder': 'Given Name', 'class':'form-control form-control-sm', 'id':'creator'}))
    familyname = forms.CharField(label='Family Name', widget=forms.TextInput(attrs={'placeholder': 'Family Name', 'class':'form-control form-control-sm', 'id':'creator'}))
    orcid = forms.CharField(label='Name Identifier',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Orcid Id', 'class':'form-control form-control-sm', 'id':'creator'}))
    affiliation = forms.CharField(label='Affiliation',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Affiliation', 'class':'form-control form-control-sm', 'id':'creator'}))
   
CreatorFormset = formset_factory(CreatorForm, extra=0,  min_num=1, validate_min=True)
class FunderForm(forms.Form):
    funder_name = forms.CharField(label='Funder Name', widget=forms.TextInput(attrs={'placeholder': 'Funder Name', 'class':'form-control form-control-sm search-input', 'id':'funder'}))
    funder_identifier = forms.CharField(label='Funder Identifier', widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Funder Identifier', 'class':'form-control form-control-sm funder_id', 'id':'funder'}))
    award_number = forms.CharField(label='Award Number',  required=False,  widget=forms.TextInput(attrs={'placeholder': 'Award Number', 'class':'form-control form-control-sm', 'id':'funder'}))
    award_title = forms.CharField(label='Award Title',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Award Title', 'class':'form-control form-control-sm', 'id':'funder'}))
   
FunderFormset = formset_factory(FunderForm, extra=0,  min_num=1, validate_min=True)

class UrlForm(forms.Form):
    url = forms.CharField(label='Url', widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'id':'url'}))

class AddUrlForm(forms.Form):
    add_url = forms.CharField(label='Add Url', widget=forms.TextInput(attrs={'placeholder': 'Assign url to doi', 'class':'form-control form-control-sm', 'id':'addUrl'}))



