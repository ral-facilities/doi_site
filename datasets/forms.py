from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory, MultiWidget, TextInput
from doi_site.local_settings import DOI_PREFIX
from mds.MdsApi import MdsApi

RT_CHOICES = [
    (None, 'Select resource type..'),
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
RIT_CHOICES = [
(None, 'Select identifier type..'),
('ARK', 'ARK'),
('arXiv', 'arXiv'),
('bibcode', 'bibcode'),
('DOI', 'DOI'),
('EAN13', 'EAN13'),
('EISSN', 'EISSN'),
('Handle', 'Handle'),
('IGSN', 'IGSN'),
('ISBN', 'ISBN'),
('ISSN', 'ISSN'),
('ISTC', 'ISTC'),
('LISSN', 'LISSN'),
('LSID', 'LSID'),
('PMID', 'PMID'),
('PURL', 'PURL'),
('UPC', 'UPC'),
('URL', 'URL'),
('URN', 'URN'),
('w3id', 'w3id')
]
RIRT_CHOICES = [
(None, 'Select relation type..'),
('IsCitedBy', 'IsCitedBy'),
('Cites', 'Cites'),
('IsSupplementTo', 'IsSupplementTo'),
('IsSupplementedBy', 'IsSupplementedBy'),
('IsContinuedBy', 'IsContinuedBy'),
('Continues', 'Continues'),
('IsDescribedBy', 'IsDescribedBy'),
('Describes', 'Describes'),
('HasMetadata', 'HasMetadata'),
('IsMetadataFor', 'IsMetadataFor'),
('HasVersion', 'HasVersion'),
('IsVersionOf', 'IsVersionOf'),
('IsNewVersionOf', 'IsNewVersionOf'),
('IsPreviousVersionOf', 'IsPreviousVersionOf'),
('IsPartOf', 'IsPartOf'),
('HasPart', 'HasPart'),
('IsPublishedIn', 'IsPublishedIn'),
('IsReferencedBy', 'IsReferencedBy'),
('References', 'References'),
('IsDocumentedBy', 'IsDocumentedBy'),
('Documents', 'Documents'),
('IsCompiledBy', 'IsCompiledBy'),
('Compiles', 'Compiles'),
('IsVariantFormOf', 'IsVariantFormOf'),
('IsOriginalFormOf', 'IsOriginalFormOf'),
('IsIdenticalTo', 'IsIdenticalTo'),
('IsReviewedBy', 'IsReviewedBy'),
('Reviews', 'Reviews'),
('IsDerivedFrom', 'IsDerivedFrom'),
('IsSourceOf', 'IsSourceOf'),
('IsRequiredBy', 'IsRequiredBy'),
('Requires', 'Requires'),
('IsObsoletedBy', 'IsObsoletedBy'),
('Obsoletes', 'Obsoletes')
]
DT_CHOICES = [
(None, 'Select date type..'),
('Accepted', 'Accepted'),
('Available', 'Available'),
('Copyrighted', 'Copyrighted'),
('Collected', 'Collected'),
('Created', 'Created'),
('Issued', 'Issued'),
('Submitted', 'Submitted'),
('Updated', 'Updated'),
('Valid', 'Valid'),
('Withdrawn', 'Withdrawn'),
('Other', 'Other')
]

class DoiForm(forms.Form):
    identifier = forms.CharField(label='Identifier', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'DOI', 'class':'form-control form-control-sm', 'id':'identifier'}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'form-control form-control-sm', 'id':'title'}))
    publisher = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Publisher', 'class':'form-control form-control-sm', 'id':'publisher'}))
    publication_year = forms.IntegerField(label='Pick the year:', min_value=1975, max_value=2100, widget=forms.TextInput(attrs={'placeholder': 'Publication Year', 'class':'form-control form-control-sm', 'id':'publicationYear'}))
    resource_type = forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES, attrs={'placeholder': 'lalala', 'class':'form-select form-select-sm', 'id':'resourceType'}))
    resource_type_text = forms.CharField(label='Resource type:', required=False, widget=forms.TextInput(attrs={'placeholder': 'Resource type other', 'class':'form-control form-control-sm', 'id':'resourceType'}))
    abstract = forms.CharField(label='Abstract', required=False, widget=forms.Textarea(attrs={'placeholder': 'Abstract',"rows":3, 'class':'form-control form-control-sm', 'id':'abstract'}))
    version = forms.CharField(label='Version', required=False, widget=forms.TextInput(attrs={'placeholder': 'Version', 'class':'form-control form-control-sm', 'id':'version'}))

    def __init__(self, *args, **kwargs):
        self._domains = kwargs.pop('domains', None)
        self._request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super(DoiForm, self).clean()
        identifier = self.cleaned_data.get('identifier')
        
        mdsApi = MdsApi(self._request)
        r = mdsApi.get(f'/metadata/{DOI_PREFIX}/{identifier}')
        
        if identifier in self._domains:
            self._errors['identifier'] = self.error_class(['Cannot use Sub-Domain by itself, please append with unique identifiying data'])
        elif r.status_code == 200:
            self._errors['identifier'] = self.error_class(['DOI is already registered, please use another'])

class SubjectForm(forms.Form):
     subject = forms.CharField(label='Subject', required=False, widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class':'form-control form-control-sm', 'id':'subject'}))
SubjectFormset = formset_factory(SubjectForm, extra=1)

class RelatedIdentifierForm(forms.Form):
        related_identifier = forms.CharField(label='Identifier', required=False, widget=forms.TextInput(attrs={'placeholder': 'Related identifier', 'class':'related-identifier form-control form-control-sm', 'id':'relatedIdentifier'}))
        related_identifier_type = forms.CharField(label='Pick the identifier type:', required=False, widget=forms.Select(choices=RIT_CHOICES, attrs={'class':'related-identifier-type form-select form-select-sm', 'id':'relatedIdentifier'}))
        related_identifier_relation_type = forms.CharField(label='Pick the relation type:', required=False, widget=forms.Select(choices=RIRT_CHOICES, attrs={'class':'related-identifier-relation-type form-select form-select-sm', 'id':'relatedIdentifier'}))
RelatedIdentifierFormset = formset_factory(RelatedIdentifierForm, extra=1)

class CreatorForm(forms.Form):
    givenname = forms.CharField(label='Given Name', widget=forms.TextInput(attrs={'placeholder': 'Given Name', 'class':'form-control form-control-sm', 'id':'creator'}))
    familyname = forms.CharField(label='Family Name', widget=forms.TextInput(attrs={'placeholder': 'Family Name', 'class':'form-control form-control-sm', 'id':'creator'}))
    orcid = forms.CharField(label='Name Identifier',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Orcid Id', 'class':'form-control form-control-sm', 'id':'creator'}))
    affiliation = forms.CharField(label='Affiliation',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Affiliation', 'class':'form-control form-control-sm', 'id':'creator'}))
CreatorFormset = formset_factory(CreatorForm, extra=0,  min_num=1, validate_min=True)

class FunderForm(forms.Form):
    funder_name = forms.CharField(label='Funder Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'Funder Name', 'class':'form-control form-control-sm search-input', 'id':'funder'}))
    funder_identifier = forms.CharField(label='Funder Identifier',  required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Funder Identifier', 'class':'form-control form-control-sm funder_id', 'id':'funder'}))
    award_number = forms.CharField(label='Award Number',  required=False,  widget=forms.TextInput(attrs={'placeholder': 'Award Number', 'class':'form-control form-control-sm', 'id':'funder'}))
    award_title = forms.CharField(label='Award Title',  required=False, widget=forms.TextInput(attrs={'placeholder': 'Award Title', 'class':'form-control form-control-sm', 'id':'funder'}))
FunderFormset = formset_factory(FunderForm, extra=1)

class UrlForm(forms.Form):
    url = forms.URLField(label='', required=False, widget=forms.TextInput(attrs={'placeholder':'URL', 'class':'form-control form-control-sm', 'id':'url'}))

class AddUrlForm(forms.Form):
    add_url = forms.CharField(label='Add Url', widget=forms.TextInput(attrs={'placeholder': 'Enter DOI', 'class':'form-control form-control-sm', 'id':'addUrl'}))

class DateForm(forms.Form):
    date = forms.CharField(label='Date', required=False, validators=[
            RegexValidator(
                regex='^([0-9]{4}|[\-][0-9]{4})|(([0-9]{4}|[\-][0-9]{4})[\-](0?[1-9]|1[0-2]))|(([0-9]{4}|[\-][0-9]{4})[\-](0?[1-9]|1[0-2])[\-](0?[1-9]|[12]\d|3[01]))$',
                message='The date format is not right!',
            ),
        ], widget=forms.TextInput(attrs={'placeholder': 'Date', 'class':'date form-control form-control-sm', 'id':'date'}))
    date_type = forms.CharField(label='Pick the date type:', required=False, widget=forms.Select(choices=DT_CHOICES, attrs={'class':'date-type form-select form-select-sm', 'id':'date'}))
    date_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Date Information', 'class':'form-control form-control-sm', 'id':'date'}))

DateFormset = formset_factory(DateForm, extra=1)