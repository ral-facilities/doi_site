from django import forms
from django.core.validators import RegexValidator
from django.forms import MultiWidget, TextInput

RT_CHOICES= [
    ('type 1', 'Type A'),
    ('type 2', 'Type B'),
    ('type 3', 'Type C'),
    ('type 4', 'Type D'),
    ]

    
class CreatorField(forms.MultiValueField):
    def __init__(self, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = (
            forms.CharField(
                error_messages={'incomplete': 'Enter a country calling code.'},
                validators=[
                    RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                ],
                label = "Given Name"
            ),
            forms.CharField(
                error_messages={'incomplete': 'Enter a phone number.'},
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                required=False,
            ),
        )
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=False, **kwargs
        )

class CreatorWidget(MultiWidget):
    template_name = 'creator.html'

    def __init__(self, attrs=None):
        widgets=[forms.TextInput, forms.TextInput, forms.TextInput]
        super().__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            pass
        return [None, None, None]

class SimpleForm(forms.Form):
    identifier = forms.CharField(label='Identifier', max_length=100)
    creator_given_name = forms.CharField(label='Given Name', max_length=100, widget=forms.TextInput(attrs={'class' : 'creator'}))
    creator_family_name = forms.CharField(label='Family Name', max_length=100, widget=forms.TextInput(attrs={'class' : 'creator'}))
    creator_affiliation = forms.CharField(label='Affiliation', max_length=100)
    title = forms.CharField(max_length=100)
    publisher = forms.CharField(max_length=100)
    publication_year = forms.CharField(max_length=100)
    resource_type= forms.CharField(label='Pick the resource type:', widget=forms.Select(choices=RT_CHOICES))
    subject = forms.CharField(max_length=100)
    creator = CreatorField(label='', widget = CreatorWidget())
    
